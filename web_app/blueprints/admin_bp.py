from flask import Blueprint, jsonify
from core_auth import admin_required
from db import get_db_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin_bp.get("/stats")
@admin_required
def get_stats():
    """
    Estadísticas generales del sistema para el dashboard admin.
    ---
    tags: [Admin]
    responses:
      200:
        description: Stats del sistema
      401:
        description: No autorizado
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        # ── Mediciones generales ──────────────────────────────
        cur.execute("""
            SELECT
                COUNT(*)                                                    AS total,
                COUNT(*) FILTER (WHERE timestamp >= NOW() - INTERVAL '24h') AS ultimas_24h,
                COUNT(*) FILTER (WHERE timestamp >= NOW() - INTERVAL '1h')  AS ultima_hora,
                MAX(timestamp)                                              AS ultima_medicion
            FROM oogsj_data.measurement;
        """)
        m = cur.fetchone()

        # ── Plataformas con datos (sin duplicados) ────────────
        cur.execute("""
            SELECT COUNT(DISTINCT p.id)
            FROM oogsj_data.platform p
            JOIN oogsj_data.sensor s ON s.platform_id = p.id
            JOIN oogsj_data.measurement me ON me.sensor_id = s.id;
        """)
        plats_activas = cur.fetchone()[0]

        # ── Avisos al navegante ───────────────────────────────
        cur.execute("""
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE fecha >= CURRENT_DATE - 30) AS ultimos_30d
            FROM oogsj_data.aviso_navegante;
        """)
        av = cur.fetchone()

        # ── Documentos en biblioteca ──────────────────────────
        cur.execute("SELECT COUNT(*) FROM oogsj_data.document;")
        docs = cur.fetchone()[0]

        # ── Último aviso scrapeado ────────────────────────────
        cur.execute("""
            SELECT numero, fecha, scraped_at
            FROM oogsj_data.aviso_navegante
            ORDER BY scraped_at DESC LIMIT 1;
        """)
        av_last = cur.fetchone()

    finally:
        cur.close()
        conn.close()

    return jsonify({
        "mediciones": {
            "total":         m[0],
            "ultimas_24h":   m[1],
            "ultima_hora":   m[2],
            "ultima_ts":     m[3].isoformat() if m[3] else None,
        },
        "plataformas_activas": plats_activas,
        "avisos": {
            "total":       av[0],
            "ultimos_30d": av[1],
            "ultimo": {
                "numero":     av_last[0] if av_last else None,
                "fecha":      av_last[1].isoformat() if av_last and av_last[1] else None,
                "scraped_at": av_last[2].isoformat() if av_last and av_last[2] else None,
            } if av_last else None,
        },
        "documentos": docs,
    })


@admin_bp.get("/plataformas")
@admin_required
def get_plataformas():
    """
    Estado detallado de cada plataforma: última transmisión, cantidad de mediciones.
    ---
    tags: [Admin]
    responses:
      200:
        description: Lista de plataformas con estado
      401:
        description: No autorizado
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT
                p.id,
                p.name                                  AS nombre,
                pt.name                                 AS tipo,
                COUNT(DISTINCT s.id)                    AS sensores,
                MAX(m.timestamp)                        AS ultima_transmision,
                COUNT(m.id)                             AS total_mediciones,
                COUNT(m.id) FILTER (
                    WHERE m.timestamp >= NOW() - INTERVAL '24h'
                )                                       AS mediciones_24h
            FROM oogsj_data.platform p
            LEFT JOIN oogsj_data.platform_type pt  ON pt.id = p.platform_type_id
            LEFT JOIN oogsj_data.sensor s           ON s.platform_id = p.id
            LEFT JOIN oogsj_data.measurement m      ON m.sensor_id   = s.id
            GROUP BY p.id, p.name, pt.name
            HAVING COUNT(DISTINCT s.id) > 0
            ORDER BY ultima_transmision DESC NULLS LAST;
        """)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    now_aware = __import__('datetime').datetime.utcnow()

    plataformas = []
    for r in rows:
        ultima_ts   = r[4]
        if ultima_ts:
            # Calcular horas desde última transmisión
            delta_h = (now_aware - ultima_ts).total_seconds() / 3600
            if delta_h < 2:
                estado = "ok"
            elif delta_h < 48:
                estado = "alerta"
            else:
                estado = "sin_datos"
        else:
            delta_h = None
            estado  = "sin_datos"

        plataformas.append({
            "id":                 r[0],
            "nombre":             r[1],
            "tipo":               r[2],
            "sensores":           r[3],
            "ultima_transmision": ultima_ts.isoformat() if ultima_ts else None,
            "horas_sin_datos":    round(delta_h, 1) if delta_h is not None else None,
            "total_mediciones":   r[5],
            "mediciones_24h":     r[6],
            "estado":             estado,  # "ok" | "alerta" | "sin_datos"
        })

    return jsonify({"plataformas": plataformas})
