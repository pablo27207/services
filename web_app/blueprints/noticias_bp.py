from flask import Blueprint, jsonify, request
from core_auth import admin_required
from db import get_db_connection

noticias_bp = Blueprint("noticias", __name__, url_prefix="/api/noticias")


def _serialize(r):
    return {
        "id":         r[0],
        "titulo":     r[1],
        "contenido":  r[2],
        "categoria":  r[3],
        "imagen_url": r[4],
        "publicado":  r[5],
        "created_at": r[6].isoformat() if r[6] else None,
        "updated_at": r[7].isoformat() if r[7] else None,
    }


# ── Público: lista de noticias publicadas ─────────────────────────────────
@noticias_bp.get("/")
def list_noticias():
    """
    Lista noticias publicadas (público)
    ---
    tags: [Noticias]
    parameters:
      - name: limit
        in: query
        schema: { type: integer, default: 20 }
    responses:
      200:
        description: Lista de noticias publicadas
    """
    try:
        limit = max(1, min(int(request.args.get("limit", 20)), 100))
    except Exception:
        limit = 20

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT id, titulo, contenido, categoria, imagen_url, publicado, created_at, updated_at
            FROM oogsj_data.noticia
            WHERE publicado = true
            ORDER BY created_at DESC
            LIMIT %s;
        """, (limit,))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return jsonify({"noticias": [_serialize(r) for r in rows]})


# ── Admin: lista completa ─────────────────────────────────────────────────
@noticias_bp.get("/admin")
@admin_required
def admin_list():
    """
    Lista todas las noticias (admin)
    ---
    tags: [Noticias]
    responses:
      200:
        description: Lista completa incluyendo no publicadas
      401:
        description: No autorizado
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT id, titulo, contenido, categoria, imagen_url, publicado, created_at, updated_at
            FROM oogsj_data.noticia
            ORDER BY created_at DESC;
        """)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return jsonify({"noticias": [_serialize(r) for r in rows]})


# ── Admin: crear ──────────────────────────────────────────────────────────
@noticias_bp.post("/admin")
@admin_required
def admin_create():
    """
    Crear noticia (admin)
    ---
    tags: [Noticias]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [titulo, contenido]
            properties:
              titulo:     { type: string }
              contenido:  { type: string }
              categoria:  { type: string }
              imagen_url: { type: string }
              publicado:  { type: boolean }
    responses:
      201:
        description: Noticia creada
      401:
        description: No autorizado
    """
    data      = request.get_json(silent=True) or {}
    titulo    = (data.get("titulo") or "").strip()
    contenido = (data.get("contenido") or "").strip()
    if not titulo or not contenido:
        return jsonify({"error": "titulo y contenido son obligatorios"}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO oogsj_data.noticia (titulo, contenido, categoria, imagen_url, publicado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, titulo, contenido, categoria, imagen_url, publicado, created_at, updated_at;
        """, (titulo, contenido,
              data.get("categoria") or None,
              data.get("imagen_url") or None,
              bool(data.get("publicado", False))))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    return jsonify(_serialize(row)), 201


# ── Admin: editar ─────────────────────────────────────────────────────────
@noticias_bp.put("/admin/<int:nid>")
@admin_required
def admin_update(nid: int):
    """
    Editar noticia (admin)
    ---
    tags: [Noticias]
    parameters:
      - name: nid
        in: path
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Noticia actualizada
      404:
        description: No encontrada
    """
    data = request.get_json(silent=True) or {}
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            UPDATE oogsj_data.noticia
            SET titulo     = COALESCE(%s, titulo),
                contenido  = COALESCE(%s, contenido),
                categoria  = %s,
                imagen_url = %s,
                publicado  = COALESCE(%s, publicado),
                updated_at = NOW()
            WHERE id = %s
            RETURNING id, titulo, contenido, categoria, imagen_url, publicado, created_at, updated_at;
        """, (data.get("titulo") or None,
              data.get("contenido") or None,
              data.get("categoria") or None,
              data.get("imagen_url") or None,
              data.get("publicado") if "publicado" in data else None,
              nid))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify(_serialize(row))


# ── Admin: eliminar ───────────────────────────────────────────────────────
@noticias_bp.delete("/admin/<int:nid>")
@admin_required
def admin_delete(nid: int):
    """
    Eliminar noticia (admin)
    ---
    tags: [Noticias]
    parameters:
      - name: nid
        in: path
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Noticia eliminada
      404:
        description: No encontrada
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("DELETE FROM oogsj_data.noticia WHERE id = %s RETURNING id;", (nid,))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404
    return jsonify({"ok": True, "id": nid})
