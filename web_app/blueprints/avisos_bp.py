from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify, request

from db import get_db_connection

avisos_bp = Blueprint("avisos", __name__, url_prefix="/api/avisos")


@avisos_bp.get("/navegante")
def get_avisos_navegante():
    """
    Avisos al navegante — últimos 30 días filtrados por Golfo San Jorge / Chubut
    ---
    tags: [Avisos]
    parameters:
      - name: limit
        in: query
        schema: { type: integer, default: 20, maximum: 100 }
        description: Cantidad máxima de avisos a devolver
    responses:
      200:
        description: Lista de avisos del navegante relevantes para la región
        content:
          application/json:
            schema:
              type: object
              properties:
                total:
                  type: integer
                avisos:
                  type: array
                  items:
                    type: object
                    properties:
                      id:         { type: integer }
                      numero:     { type: string, example: "0024-2026" }
                      fecha:      { type: string, format: date }
                      tipo:       { type: string, example: "COSTERO O" }
                      texto_es:   { type: string }
                      texto_en:   { type: string }
                      fuente:     { type: string }
                      scraped_at: { type: string, format: date-time }
      500:
        description: Error interno
    """
    try:
        limit = max(1, min(int(request.args.get("limit", 20)), 100))
    except Exception:
        limit = 20

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        desde = datetime.now(timezone.utc) - timedelta(days=90)
        cur.execute("""
            SELECT id, numero, fecha, tipo, texto_es, texto_en, fuente, scraped_at
            FROM oogsj_data.aviso_navegante
            WHERE fecha >= %s
            ORDER BY fecha DESC, scraped_at DESC
            LIMIT %s;
        """, (desde.date(), limit))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    avisos = [
        {
            "id":         r[0],
            "numero":     r[1],
            "fecha":      r[2].isoformat() if r[2] else None,
            "tipo":       r[3],
            "texto_es":   r[4],
            "texto_en":   r[5],
            "fuente":     r[6],
            "scraped_at": r[7].isoformat() if r[7] else None,
        }
        for r in rows
    ]

    return jsonify({"total": len(avisos), "avisos": avisos})


@avisos_bp.get("/navegante/latest")
def get_aviso_latest():
    """
    Aviso al navegante más reciente
    ---
    tags: [Avisos]
    responses:
      200:
        description: Último aviso registrado
      404:
        description: Sin avisos disponibles
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT id, numero, fecha, tipo, texto_es, texto_en, fuente, scraped_at
            FROM oogsj_data.aviso_navegante
            ORDER BY fecha DESC, scraped_at DESC
            LIMIT 1;
        """)
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "Sin avisos disponibles"}), 404

    return jsonify({
        "id":         row[0],
        "numero":     row[1],
        "fecha":      row[2].isoformat() if row[2] else None,
        "tipo":       row[3],
        "texto_es":   row[4],
        "texto_en":   row[5],
        "fuente":     row[6],
        "scraped_at": row[7].isoformat() if row[7] else None,
    })