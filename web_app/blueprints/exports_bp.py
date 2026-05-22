import os
import re
from datetime import datetime
from pathlib import Path

from celery import Celery
from flask import Blueprint, jsonify, request, send_file

import config
from core_auth import admin_required

exports_bp = Blueprint("exports", __name__, url_prefix="/api/exports")

_MONTH_NAMES = {
    1: "Enero", 2: "Febrero", 3: "Marzo",    4: "Abril",
    5: "Mayo",  6: "Junio",   7: "Julio",    8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

_FILE_RE = re.compile(r"^(\d{4})_(\d{2})_.+\.csv$")


def _human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def _scan_exports(platform_filter: str = None, year_filter: int = None) -> list[dict]:
    """Recorre EXPORTS_FOLDER y devuelve metadata de cada CSV encontrado."""
    root = Path(config.EXPORTS_FOLDER)
    if not root.exists():
        return []

    platforms = []
    for platform_dir in sorted(root.iterdir()):
        if not platform_dir.is_dir():
            continue
        if platform_filter and platform_dir.name != platform_filter:
            continue

        files = []
        for year_dir in sorted(platform_dir.iterdir()):
            if not year_dir.is_dir():
                continue
            if year_filter and year_dir.name != str(year_filter):
                continue

            for f in sorted(year_dir.iterdir()):
                if not f.is_file() or f.suffix != ".csv":
                    continue
                m = _FILE_RE.match(f.name)
                if not m:
                    continue
                year  = int(m.group(1))
                month = int(m.group(2))
                stat  = f.stat()
                rel   = f.relative_to(root).as_posix()
                files.append({
                    "filename":     f.name,
                    "year":         year,
                    "month":        month,
                    "month_name":   _MONTH_NAMES.get(month, ""),
                    "size_bytes":   stat.st_size,
                    "size_human":   _human_size(stat.st_size),
                    "generated_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "download_url": f"/api/exports/download/{rel}",
                })

        if files:
            platforms.append({"slug": platform_dir.name, "files": files})

    return platforms


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@exports_bp.get("/")
def list_exports():
    """
    Listar archivos CSV exportados
    ---
    tags: [Exports]
    summary: Lista todos los archivos CSV generados, agrupados por plataforma
    parameters:
      - name: platform
        in: query
        required: false
        schema: { type: string }
        description: Slug de plataforma (ej. boya_cidmar_2)
      - name: year
        in: query
        required: false
        schema: { type: integer }
        description: Filtrar por año (ej. 2026)
    responses:
      200:
        description: Lista de archivos disponibles
        content:
          application/json:
            schema:
              type: object
              properties:
                total_files:
                  type: integer
                  example: 10
                platforms:
                  type: array
                  items:
                    type: object
                    properties:
                      slug:  { type: string, example: boya_cidmar_2 }
                      files:
                        type: array
                        items:
                          type: object
                          properties:
                            filename:     { type: string, example: "2026_04_boya_cidmar_2.csv" }
                            year:         { type: integer, example: 2026 }
                            month:        { type: integer, example: 4 }
                            month_name:   { type: string,  example: Abril }
                            size_bytes:   { type: integer, example: 45678 }
                            size_human:   { type: string,  example: "44.6 KB" }
                            generated_at: { type: string,  format: date-time }
                            download_url: { type: string,  example: "/api/exports/download/boya_cidmar_2/2026/2026_04_boya_cidmar_2.csv" }
    """
    platforms = _scan_exports(
        platform_filter=request.args.get("platform"),
        year_filter=request.args.get("year", type=int),
    )
    total = sum(len(p["files"]) for p in platforms)
    return jsonify({"total_files": total, "platforms": platforms})


@exports_bp.get("/download/<path:filepath>")
def download_export(filepath: str):
    """
    Descargar un archivo CSV exportado
    ---
    tags: [Exports]
    summary: Descarga un CSV por su ruta relativa dentro del directorio de exports
    parameters:
      - name: filepath
        in: path
        required: true
        schema: { type: string }
        description: "Ruta relativa (ej. boya_cidmar_2/2026/2026_04_boya_cidmar_2.csv)"
    responses:
      200:
        description: Archivo CSV
        content:
          text/csv:
            schema: { type: string, format: binary }
      403:
        description: Ruta fuera del directorio permitido
      404:
        description: Archivo no encontrado
    """
    exports_root = Path(config.EXPORTS_FOLDER).resolve()
    target = (exports_root / filepath).resolve()

    try:
        target.relative_to(exports_root)
    except ValueError:
        return jsonify({"error": "forbidden_path"}), 403

    if not target.is_file():
        return jsonify({"error": "not_found"}), 404

    return send_file(
        str(target),
        mimetype="text/csv",
        as_attachment=True,
        download_name=target.name,
    )


@exports_bp.post("/generate")
@admin_required
def trigger_generate():
    """
    Disparar generación manual de exports (solo admin)
    ---
    tags: [Exports]
    summary: Encola la tarea de generación de CSV en el worker de Celery
    requestBody:
      required: false
      content:
        application/json:
          schema:
            type: object
            properties:
              year:
                type: integer
                example: 2026
                description: Año a exportar (omitir para usar el mes anterior)
              month:
                type: integer
                example: 4
                description: Mes a exportar (omitir para usar el mes anterior)
    responses:
      202:
        description: Tarea encolada correctamente
        content:
          application/json:
            schema:
              type: object
              properties:
                ok:      { type: boolean, example: true }
                task_id: { type: string }
                message: { type: string }
      401:
        description: No autorizado
      503:
        description: No se pudo conectar al broker de tareas
    """
    body  = request.get_json(silent=True) or {}
    year  = body.get("year")
    month = body.get("month")

    broker = os.getenv("REDIS_URL", "redis://cache:6379") + "/0"
    try:
        celery_client = Celery(broker=broker)
        task = celery_client.send_task(
            "celery_tasks.monthly_csv_export",
            kwargs={"year": year, "month": month},
        )
    except Exception as exc:
        return jsonify({"ok": False, "error": f"No se pudo encolar la tarea: {exc}"}), 503

    label = f"{year}-{month:02d}" if (year and month) else "mes anterior"
    return jsonify({
        "ok":      True,
        "task_id": task.id,
        "message": f"Exportación de {label} encolada (task_id={task.id})",
    }), 202
