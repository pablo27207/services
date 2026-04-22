import re
import uuid
from pathlib import Path

from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename

from core_auth import admin_required
from config import UPLOAD_FOLDER, ALLOWED_MIMES, MAX_UPLOAD_BYTES
from db import get_db_connection

library_bp = Blueprint("library", __name__, url_prefix="/api/library")


def _parse_pagination():
    try:
        limit = max(1, min(int(request.args.get("limit", 10)), 100))
    except Exception:
        limit = 10
    try:
        page = max(1, int(request.args.get("page", 1)))
    except Exception:
        page = 1
    return limit, page, (page - 1) * limit


_SORT_MAP = {
    "year_desc":      "d.year DESC NULLS LAST, COALESCE(d.citations,0) DESC, d.title ASC",
    "year_asc":       "d.year ASC  NULLS FIRST, d.title ASC",
    "citations_desc": "COALESCE(d.citations,0) DESC, d.year DESC NULLS LAST, d.title ASC",
    "citations_asc":  "COALESCE(d.citations,0) ASC,  d.year DESC NULLS LAST, d.title ASC",
    "title_asc":      "d.title ASC NULLS LAST",
}
_DEFAULT_SORT = _SORT_MAP["year_desc"]

_AUTHORS_AGG = """
    COALESCE(
        json_agg(
            json_build_object('id', a.id, 'full_name', a.full_name)
            ORDER BY da.author_order
        ) FILTER (WHERE a.id IS NOT NULL),
        '[]'::json
    ) AS authors
"""


def _serialize_row(r):
    doc_id, title, year, venue, citations, url, doi, has_local_file, authors_json = r
    return {
        "id": doc_id, "title": title, "year": year, "venue": venue,
        "doi": doi, "url": url, "citations": citations,
        "authors": authors_json or [],
        "has_local_file": bool(has_local_file),
        "canonical_id": doc_id, "is_duplicate": False,
    }


@library_bp.get("/list")
def library_list():
    """
    Listar documentos (paginado)
    ---
    tags: [Library]
    parameters:
      - name: page
        in: query
        schema: { type: integer, default: 1 }
      - name: limit
        in: query
        schema: { type: integer, default: 10, maximum: 100 }
      - name: sort
        in: query
        schema:
          type: string
          enum: [year_desc, year_asc, citations_desc, citations_asc, title_asc]
          default: year_desc
    responses:
      200:
        description: Lista paginada de documentos científicos
        content:
          application/json:
            schema:
              type: object
              properties:
                page:  { type: integer }
                limit: { type: integer }
                total: { type: integer }
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      id:             { type: integer }
                      title:          { type: string }
                      year:           { type: integer }
                      venue:          { type: string }
                      citations:      { type: integer }
                      doi:            { type: string }
                      url:            { type: string }
                      has_local_file: { type: boolean }
                      authors:
                        type: array
                        items:
                          type: object
                          properties:
                            id:        { type: integer }
                            full_name: { type: string }
    """
    limit, page, offset = _parse_pagination()
    order_by = _SORT_MAP.get((request.args.get("sort") or "").lower(), _DEFAULT_SORT)

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM oogsj_data.document;")
        total = cur.fetchone()[0]
        cur.execute(f"""
            SELECT d.id, d.title, d.year, d.venue,
                   COALESCE(d.citations,0), d.url, d.doi,
                   (d.storage_path IS NOT NULL),
                   {_AUTHORS_AGG}
            FROM oogsj_data.document d
            LEFT JOIN oogsj_data.document_author da ON da.document_id = d.id
            LEFT JOIN oogsj_data.author a           ON a.id = da.author_id
            GROUP BY d.id
            ORDER BY {order_by}
            LIMIT %s OFFSET %s;
        """, (limit, offset))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return jsonify({"page": page, "limit": limit, "total": total,
                    "items": [_serialize_row(r) for r in rows]})


@library_bp.get("/search")
def library_search():
    """
    Buscar documentos
    ---
    tags: [Library]
    parameters:
      - name: q
        in: query
        schema: { type: string }
        description: Texto libre — busca en título, venue, DOI, URL y autores
      - name: page
        in: query
        schema: { type: integer, default: 1 }
      - name: limit
        in: query
        schema: { type: integer, default: 10 }
      - name: year_min
        in: query
        schema: { type: integer }
      - name: year_max
        in: query
        schema: { type: integer }
      - name: has_doi
        in: query
        schema: { type: string, enum: [true, false] }
      - name: has_file
        in: query
        schema: { type: string, enum: [true, false] }
      - name: sort
        in: query
        schema:
          type: string
          enum: [year_desc, year_asc, citations_desc, citations_asc, title_asc]
    responses:
      200:
        description: Resultados de búsqueda paginados
    """
    q        = (request.args.get("q") or "").strip()
    limit, page, offset = _parse_pagination()
    order_by = _SORT_MAP.get((request.args.get("sort") or "").lower(), _DEFAULT_SORT)

    year_min = request.args.get("year_min")
    year_max = request.args.get("year_max")
    has_doi  = request.args.get("has_doi")
    has_file = request.args.get("has_file")

    where_parts = ["1=1"]
    params      = []

    if q:
        where_parts.append(
            "(d.title ILIKE %s OR d.venue ILIKE %s OR "
            "d.doi ILIKE %s OR d.url ILIKE %s OR a.full_name ILIKE %s)"
        )
        pat = f"%{q}%"
        params.extend([pat, pat, pat, pat, pat])

    if year_min and year_min.isdigit():
        where_parts.append("d.year >= %s"); params.append(int(year_min))
    if year_max and year_max.isdigit():
        where_parts.append("d.year <= %s"); params.append(int(year_max))
    if has_doi == "true":
        where_parts.append("d.doi IS NOT NULL")
    elif has_doi == "false":
        where_parts.append("d.doi IS NULL")
    if has_file == "true":
        where_parts.append("d.storage_path IS NOT NULL")
    elif has_file == "false":
        where_parts.append("d.storage_path IS NULL")

    where_sql = " AND ".join(where_parts)

    looks_like_doi   = bool(re.match(r"^\s*10\.\S+$", q)) if q else False
    relevance_prefix = ""
    doi_param        = None
    if looks_like_doi:
        relevance_prefix = "CASE WHEN lower(d.doi) = lower(%s) THEN 0 ELSE 1 END, "
        doi_param = q

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute(f"""
            SELECT COUNT(DISTINCT d.id)
            FROM oogsj_data.document d
            LEFT JOIN oogsj_data.document_author da ON da.document_id = d.id
            LEFT JOIN oogsj_data.author a           ON a.id = da.author_id
            WHERE {where_sql};
        """, params)
        total = cur.fetchone()[0]

        page_params = list(params)
        if doi_param:
            page_params.insert(0, doi_param)
        page_params.extend([limit, offset])

        cur.execute(f"""
            SELECT d.id, d.title, d.year, d.venue,
                   COALESCE(d.citations,0), d.url, d.doi,
                   (d.storage_path IS NOT NULL),
                   {_AUTHORS_AGG}
            FROM oogsj_data.document d
            LEFT JOIN oogsj_data.document_author da ON da.document_id = d.id
            LEFT JOIN oogsj_data.author a           ON a.id = da.author_id
            WHERE {where_sql}
            GROUP BY d.id
            ORDER BY {relevance_prefix}{order_by}
            LIMIT %s OFFSET %s;
        """, page_params)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return jsonify({"q": q, "page": page, "limit": limit, "total": total,
                    "items": [_serialize_row(r) for r in rows]})


@library_bp.get("/<int:doc_id>")
def library_detail(doc_id: int):
    """
    Detalle de un documento
    ---
    tags: [Library]
    parameters:
      - name: doc_id
        in: path
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Documento completo con autores y URL de descarga
      404:
        description: Documento no encontrado
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute(f"""
            SELECT d.id, d.title, d.year, d.venue,
                   COALESCE(d.citations,0), d.url, d.doi, d.storage_path,
                   {_AUTHORS_AGG}
            FROM oogsj_data.document d
            LEFT JOIN oogsj_data.document_author da ON da.document_id = d.id
            LEFT JOIN oogsj_data.author a           ON a.id = da.author_id
            WHERE d.id = %s
            GROUP BY d.id;
        """, (doc_id,))
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    doc_id, title, year, venue, citations, url, doi, storage_path, authors_json = row
    has_file = bool(storage_path)
    return jsonify({
        "id": doc_id, "title": title, "year": year, "venue": venue,
        "doi": doi, "url": url, "citations": citations,
        "authors": authors_json or [],
        "has_local_file": has_file,
        "download_url": f"/api/library/file/{doc_id}" if has_file else None,
        "canonical_id": doc_id, "is_duplicate": False,
    })


@library_bp.get("/file/<int:doc_id>")
def library_file_download(doc_id: int):
    """
    Descargar PDF de un documento
    ---
    tags: [Library]
    parameters:
      - name: doc_id
        in: path
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Archivo PDF
        content:
          application/pdf:
            schema:
              type: string
              format: binary
      403:
        description: Ruta fuera del directorio permitido
      404:
        description: Documento o archivo no encontrado
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT storage_path, title FROM oogsj_data.document
            WHERE id = %s LIMIT 1;
        """, (doc_id,))
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    storage_path, title = row
    if not storage_path:
        return jsonify({"error": "no_local_file"}), 404

    uploads_root = Path(UPLOAD_FOLDER).resolve()
    file_path    = Path(storage_path).resolve()
    try:
        file_path.relative_to(uploads_root)
    except Exception:
        return jsonify({"error": "forbidden_path"}), 403

    if not file_path.exists():
        return jsonify({"error": "file_missing"}), 404

    return send_file(str(file_path), mimetype="application/pdf",
                     as_attachment=True,
                     download_name=f"{secure_filename(title or 'document')}.pdf",
                     max_age=3600)


@library_bp.post("/upload")
@admin_required
def library_upload():
    """
    Subir documento PDF (solo admin)
    ---
    tags: [Library]
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            required: [file, title]
            properties:
              file:    { type: string, format: binary }
              title:   { type: string }
              year:    { type: integer }
              venue:   { type: string }
              doi:     { type: string }
              url:     { type: string }
              authors:
                type: string
                description: "Autores separados por punto y coma"
    responses:
      201:
        description: Documento subido correctamente
      401:
        description: No autorizado
      413:
        description: Archivo demasiado grande
      415:
        description: Tipo de archivo no permitido
    """
    if request.content_length and request.content_length > MAX_UPLOAD_BYTES:
        return jsonify({"error": "Archivo demasiado grande (>50 MB)"}), 413

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Falta el archivo 'file'"}), 400
    if file.mimetype not in ALLOWED_MIMES:
        return jsonify({"error": f"Tipo no permitido: {file.mimetype}"}), 415

    title = (request.form.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Falta 'title'"}), 400

    year    = request.form.get("year")
    venue   = request.form.get("venue")
    doi     = request.form.get("doi")
    url     = request.form.get("url")
    authors = [a.strip() for chunk in (request.form.get("authors") or "").split(";")
               for a in chunk.split(",") if a.strip()]

    filename = f"{secure_filename(title) or 'document'}-{uuid.uuid4().hex}.pdf"
    dst_path = Path(UPLOAD_FOLDER) / filename
    file.save(dst_path)

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO oogsj_data.document (title, year, venue, citations, url, doi, storage_path)
            VALUES (%s, %s, %s, 0, %s, %s, %s) RETURNING id;
        """, (title, int(year) if (year and year.isdigit()) else None,
               venue or None, url or None, doi or None, str(dst_path)))
        doc_id = cur.fetchone()[0]

        for i, full_name in enumerate(authors, 1):
            cur.execute("""
                INSERT INTO oogsj_data.author (full_name) VALUES (%s)
                ON CONFLICT (full_name) DO UPDATE SET full_name = EXCLUDED.full_name
                RETURNING id;
            """, (full_name,))
            author_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO oogsj_data.document_author (document_id, author_id, author_order)
                VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;
            """, (doc_id, author_id, i))

        cur.execute("""
            INSERT INTO oogsj_data.document_source
                (document_id, source_type, uploaded_by, source_name, raw_payload)
            VALUES (%s, 'user_upload', NULL, 'carga manual', NULL);
        """, (doc_id,))
        conn.commit()
        cur.close()

        return jsonify({"ok": True, "data": {
            "id": doc_id, "title": title,
            "year": int(year) if (year and year.isdigit()) else None,
            "venue": venue, "doi": doi, "url": url,
            "file_url": f"/files/{filename}",
        }}), 201

    except Exception as e:
        conn.rollback()
        dst_path.unlink(missing_ok=True)
        print(f"❌ ERROR /api/library/upload: {e}")
        return jsonify({"ok": False, "error": "No se pudo guardar el documento"}), 500
    finally:
        conn.close()


@library_bp.get("/admin/list")
@admin_required
def library_admin_list():
    """
    Lista admin de documentos (solo admin)
    ---
    tags: [Library]
    parameters:
      - name: page
        in: query
        schema: { type: integer, default: 1 }
      - name: limit
        in: query
        schema: { type: integer, default: 20 }
    responses:
      200:
        description: Lista completa con storage_path y created_at
      401:
        description: No autorizado
    """
    limit, page, offset = _parse_pagination()
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT id, title, year, venue, COALESCE(citations,0),
                   url, doi, storage_path, created_at
            FROM oogsj_data.document
            ORDER BY created_at DESC LIMIT %s OFFSET %s;
        """, (limit, offset))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    return jsonify({"page": page, "limit": limit, "items": [{
        "id": r[0], "title": r[1], "year": r[2], "venue": r[3],
        "citations": r[4], "url": r[5], "doi": r[6],
        "storage_path": r[7],
        "created_at": r[8].isoformat() if r[8] else None,
    } for r in rows]})