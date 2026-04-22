from flask import Blueprint, jsonify, request
from core_auth import admin_required
from db import get_db_connection

especies_bp = Blueprint("especies", __name__, url_prefix="/api/especies")


def _serialize(r):
    return {
        "id":                 r[0],
        "nombre_comun":       r[1],
        "nombre_cientifico":  r[2],
        "descripcion":        r[3],
        "categoria":          r[4],
        "imagen_url":         r[5],
        "created_at":         r[6].isoformat() if r[6] else None,
        "updated_at":         r[7].isoformat() if r[7] else None,
    }


# ── Público: lista de especies ────────────────────────────────────────────
@especies_bp.get("/")
def list_especies():
    """
    Lista de especies del catálogo (público)
    ---
    tags: [Especies]
    parameters:
      - name: categoria
        in: query
        schema: { type: string }
      - name: q
        in: query
        schema: { type: string }
        description: Búsqueda por nombre común o científico
    responses:
      200:
        description: Lista de especies
    """
    q         = (request.args.get("q") or "").strip()
    categoria = (request.args.get("categoria") or "").strip()

    where, params = ["1=1"], []
    if q:
        where.append("(nombre_comun ILIKE %s OR nombre_cientifico ILIKE %s)")
        params += [f"%{q}%", f"%{q}%"]
    if categoria:
        where.append("categoria = %s")
        params.append(categoria)

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute(f"""
            SELECT id, nombre_comun, nombre_cientifico, descripcion, categoria, imagen_url, created_at, updated_at
            FROM oogsj_data.especie
            WHERE {' AND '.join(where)}
            ORDER BY nombre_comun ASC;
        """, params)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return jsonify({"especies": [_serialize(r) for r in rows]})


# ── Admin: crear ──────────────────────────────────────────────────────────
@especies_bp.post("/admin")
@admin_required
def admin_create():
    """
    Crear especie (admin)
    ---
    tags: [Especies]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [nombre_comun]
            properties:
              nombre_comun:      { type: string }
              nombre_cientifico: { type: string }
              descripcion:       { type: string }
              categoria:         { type: string }
              imagen_url:        { type: string }
    responses:
      201:
        description: Especie creada
      401:
        description: No autorizado
    """
    data         = request.get_json(silent=True) or {}
    nombre_comun = (data.get("nombre_comun") or "").strip()
    if not nombre_comun:
        return jsonify({"error": "nombre_comun es obligatorio"}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO oogsj_data.especie
                (nombre_comun, nombre_cientifico, descripcion, categoria, imagen_url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, nombre_comun, nombre_cientifico, descripcion, categoria, imagen_url, created_at, updated_at;
        """, (nombre_comun,
              data.get("nombre_cientifico") or None,
              data.get("descripcion") or None,
              data.get("categoria") or None,
              data.get("imagen_url") or None))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    return jsonify(_serialize(row)), 201


# ── Admin: editar ─────────────────────────────────────────────────────────
@especies_bp.put("/admin/<int:eid>")
@admin_required
def admin_update(eid: int):
    """
    Editar especie (admin)
    ---
    tags: [Especies]
    parameters:
      - name: eid
        in: path
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Especie actualizada
      404:
        description: No encontrada
    """
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            UPDATE oogsj_data.especie
            SET nombre_comun      = COALESCE(%s, nombre_comun),
                nombre_cientifico = %s,
                descripcion       = %s,
                categoria         = %s,
                imagen_url        = %s,
                updated_at        = NOW()
            WHERE id = %s
            RETURNING id, nombre_comun, nombre_cientifico, descripcion, categoria, imagen_url, created_at, updated_at;
        """, (data.get("nombre_comun") or None,
              data.get("nombre_cientifico") or None,
              data.get("descripcion") or None,
              data.get("categoria") or None,
              data.get("imagen_url") or None,
              eid))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(_serialize(row))


# ── Admin: eliminar ───────────────────────────────────────────────────────
@especies_bp.delete("/admin/<int:eid>")
@admin_required
def admin_delete(eid: int):
    """
    Eliminar especie (admin)
    ---
    tags: [Especies]
    parameters:
      - name: eid
        in: path
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Especie eliminada
      404:
        description: No encontrada
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("DELETE FROM oogsj_data.especie WHERE id = %s RETURNING id;", (eid,))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"ok": True, "id": eid})
