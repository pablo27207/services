
#----------Con esto debo hacer mi backend ---------------------------------------------#
from flask import Flask, jsonify, render_template, request
import psycopg2
import os
import math
import requests
import time
import hashlib
from flask_mail import Mail, Message
from flask import Blueprint
from datetime import datetime, timedelta

from pathlib import Path
from werkzeug.utils import secure_filename
import uuid




app = Flask(__name__)


# Carpeta donde guardar PDFs (montada en el contenedor)
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "/app/uploads")
Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

ALLOWED_MIMES = {"application/pdf"}
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB

def allowed_file(filename, mimetype):
    ext_ok = "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS
    return ext_ok or (mimetype in ALLOWED_MIMES)

# Servir archivos subidos en dev (en prod lo hace Nginx con alias)
@app.route("/files/<path:filename>")
def serve_uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)


#------------Para enviar emails--------------------------------------
# 🔧 Configuración de correo (ejemplo con Gmail)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'gfranco323@gmail.com'
app.config['MAIL_PASSWORD'] = 'edfzzbicbaynuenl'
app.config['MAIL_DEFAULT_SENDER'] = 'gfranco323@gmail.com'


mail = Mail(app)


@app.route('/api/send-suggestion', methods=['POST'])
def send_suggestion():
    data = request.get_json()

    suggestion = data.get('message', '').strip()
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip()
    entidad = data.get('entidad', '').strip()

    if not all([suggestion, nombre, email, entidad]):
        return jsonify({
            "status": "error",
            "message": "Faltan datos obligatorios para enviar la sugerencia"
        }), 400

    try:
        msg = Message(f"Sugerencia de {nombre}",
                      sender=email,
                      recipients=['franco.garcia@conocimiento.gob.ar'])

        # 🔧 Esta es la parte que no estaba funcionando antes
        msg.body = f"""📝 Nueva sugerencia recibida:

👤 Nombre: {nombre}
🏢 Entidad: {entidad}
📧 Email: {email}

💬 Mensaje:
{suggestion}
""".strip()

        mail.send(msg)

        return jsonify({"status": "success", "message": "Sugerencia enviada con éxito"}), 200

    except Exception as e:
        print("❌ Error al enviar el correo:", e)
        return jsonify({
            "status": "error",
            "message": "Ocurrió un error al enviar la sugerencia"
        }), 500


#-------------------------------------------------------------------


# Configuración de la base de datos
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",  # Nombre del servicio en Docker
    "port": 5432
}

# Conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

# Ruta principal para mostrar la web con D3.js
@app.route("/")
def index():
    return render_template("index.html")

# Ruta para obtener los datos del mareógrafo en formato JSON
@app.route("/api/mareograph")
def get_mareograph_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id = 1 AND timestamp >= NOW() - INTERVAL '30 days'
        ORDER BY timestamp;
    """)
    
    data = [{"timestamp": row[0], "level": safe_float(row[1])} for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return jsonify(data)


# Ruta para obtener datos de la boya en JSON


@app.route("/api/buoy")
def get_buoy_data():
    conn = get_db_connection()
    cur = conn.cursor()

    sensor_ids = {
        3: "Altura de Olas",
        4: "Periodo de Olas",
        5: "Dirección de Olas",
        6: "Velocidad de Corriente",
        7: "Dirección de la Corriente",
        8: "Radiación PAR",
        9: "Batería"
    }

    diez_dias_atras = datetime.utcnow() - timedelta(days=10)

    cur.execute("""
        SELECT sensor_id, timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id IN (3, 4, 5, 6, 7, 8, 9)
          AND timestamp >= %s
        ORDER BY timestamp;
    """, (diez_dias_atras,))

    raw_data = cur.fetchall()
    cur.close()
    conn.close()

    data = {name: [] for name in sensor_ids.values()}
    for sensor_id, timestamp, value in raw_data:
        variable_name = sensor_ids.get(sensor_id, f"Sensor {sensor_id}")
        data[variable_name].append({"timestamp": timestamp, "value": value})

    return jsonify(data)




@app.route("/api/tide_forecast")
def get_tide_forecast_data():
    conn = get_db_connection()
    cur = conn.cursor()

    diez_dias_atras = datetime.utcnow() - timedelta(days=10)

    cur.execute("""
        SELECT timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id = 2
          AND timestamp >= %s
        ORDER BY timestamp;
    """, (diez_dias_atras,))
    
    data = [{"timestamp": row[0], "level": safe_float(row[1])} for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(data)

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def safe_float(val):
    try:
        f = float(val)
        return f if not math.isnan(f) else 0.0
    except:
        return 0.0


#-------------------------------------------Ultimo endpoit los ultimos datos sensados de la boya 
@app.route("/api/buoy/latest")
def get_latest_buoy_data():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (m.sensor_id)
            s.name,
            m.timestamp,
            m.value,
            u.symbol
        FROM
            oogsj_data.measurement m
        JOIN
            oogsj_data.sensor s ON m.sensor_id = s.id
        JOIN
            oogsj_data.unit u ON s.unit_id = u.id
        WHERE
            s.platform_id = 3
        ORDER BY
            m.sensor_id, m.timestamp DESC;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = {}
    for name, timestamp, value, unit in rows:
        data[name] = {
            "timestamp": timestamp,
            "value": safe_float(value) if value is not None else None,
            "unit": unit
        }

    return jsonify(data)
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.route("/api/mareograph/latest")
def get_latest_mareograph_data():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (m.sensor_id)
            s.name,
            m.timestamp,
            m.value,
            u.symbol
        FROM
            oogsj_data.measurement m
        JOIN
            oogsj_data.sensor s ON m.sensor_id = s.id
        JOIN
            oogsj_data.unit u ON s.unit_id = u.id
        WHERE
            s.platform_id = 1  -- Mareógrafo
        ORDER BY
            m.sensor_id, m.timestamp DESC;
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    data = {}
    for name, timestamp, value, unit in rows:
        data[name] = {
            "timestamp": timestamp,
            "value": safe_float(value) if value is not None else None,
            "unit": unit
        }

    return jsonify(data)

#---------------------------Estacion Meteoroloigca Comodoro Rivadavia Puerto --------------------------------------------------------------
@app.route("/api/appcr/puerto", methods=["GET"])
def get_puerto_data():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Internal Server Error - Database connection failed"}), 500

    try:
        cur = conn.cursor()

        # Filtramos por nombre de plataforma (más robusto que hardcodear un id numérico)
        cur.execute("""
            SELECT 
                s.name AS sensor,
                m."timestamp",
                m.value,
                u.symbol AS unit,
                v.name AS variable
            FROM oogsj_data.sensor s
            JOIN oogsj_data.platform p ON p.id = s.platform_id
            JOIN oogsj_data.unit u ON u.id = s.unit_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN LATERAL (
                SELECT m2."timestamp", m2.value
                FROM oogsj_data.measurement m2
                WHERE m2.sensor_id = s.id
                ORDER BY m2."timestamp" DESC
                LIMIT 1
            ) m ON TRUE
            WHERE p.name = %s
            ORDER BY s.name;
        """, ('APPCR Puerto CR',))

        data = [
            {
                "sensor": row[0],
                "timestamp": row[1].isoformat() if row[1] else None,
                "value": float(row[2]) if row[2] is not None else None,
                "unit": row[3],
                "variable": row[4],
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()
        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/puerto: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
#------------------------------Estacion al puerto mas facil ultimos dias para el grafico

@app.route("/api/appcr/puerto/history", methods=["GET"])
def get_puerto_history():
    """
    Últimos 10 días de APPCR Puerto CR, agrupados por variable.
    Formato: { "<variable>": { "unit": "<simbolo>", "data": [ {timestamp, value}, ... ] }, ... }
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Internal Server Error - Database connection failed"}), 500

    try:
        cur = conn.cursor()

        diez_dias_atras = datetime.utcnow() - timedelta(days=10)

        # Opción A (robusta): filtrar por nombre de plataforma
        cur.execute("""
            SELECT 
                v.name        AS variable_name,
                m."timestamp" AS ts,
                m.value       AS val,
                u.symbol      AS unit
            FROM oogsj_data.measurement m
            JOIN oogsj_data.sensor   s ON s.id = m.sensor_id
            JOIN oogsj_data.platform p ON p.id = s.platform_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            WHERE p.name = %s
              AND m."timestamp" >= %s
            ORDER BY v.name, m."timestamp";
        """, ('APPCR Puerto CR', diez_dias_atras))

        # ---- Opción B (si preferís por patrón en nombre de sensor, Puerto CR suele ser 160710) ----
        # cur.execute("""
        #     SELECT 
        #         v.name        AS variable_name,
        #         m."timestamp" AS ts,
        #         m.value       AS val,
        #         u.symbol      AS unit
        #     FROM oogsj_data.measurement m
        #     JOIN oogsj_data.sensor   s ON s.id = m.sensor_id
        #     JOIN oogsj_data.variable v ON v.id = s.variable_id
        #     JOIN oogsj_data.unit     u ON u.id = s.unit_id
        #     WHERE s.name LIKE '%%160710%%'
        #       AND m."timestamp" >= %s
        #     ORDER BY v.name, m."timestamp";
        # """, (diez_dias_atras,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        data = {}
        for variable_name, ts, val, unit in rows:
            bucket = data.setdefault(variable_name, {"unit": unit, "data": []})
            bucket["data"].append({
                "timestamp": ts.isoformat() if ts else None,
                "value": float(val) if val is not None else None
            })

        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/puerto/history: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


#--------------------------endpoint estacion meteorologica caleta cordova ultimos datos ----------------------------------------------------
### ESTE ES EL CORRECTO, LUEGO VER QUE METODOS SOBRAN Y COMENTARLO

@app.route("/api/appcr/muelle_cc", methods=["GET"])
def get_muelle_cc_data():
    """
    Obtiene el último registro de cada sensor de la estación "APPCR Muelle CC".
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Internal Server Error - Database connection failed"}), 500

    try:
        cur = conn.cursor()

        # Usamos una subconsulta con LATERAL JOIN para obtener el registro más reciente
        # para cada sensor que contenga el identificador '160710' en su nombre.
        cur.execute("""
            SELECT 
                s.name AS sensor,
                m.timestamp,
                m.value,
                u.symbol AS unit,
                v.name AS variable
            FROM oogsj_data.sensor s
            JOIN oogsj_data.unit u ON s.unit_id = u.id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN LATERAL (
                SELECT timestamp, value
                FROM oogsj_data.measurement
                WHERE sensor_id = s.id
                ORDER BY timestamp DESC
                LIMIT 1
            ) m ON true
            WHERE s.name LIKE '%%160710%%'
            ORDER BY s.name;
        """)

        data = [
            {
                "sensor": row[0],
                "timestamp": row[1].isoformat() if row[1] else None,
                "value": float(row[2]) if row[2] is not None else None,
                "unit": row[3],
                "variable": row[4]
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()
        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/muelle_cc: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
#--------------------------historico muelle cc este es el real --------------------------------------------
#te trae en formato json todos los datos en los ultimos 10 dias
@app.route("/api/appcr/muelle_cc/history", methods=["GET"])
def get_muelle_cc_history():
    """
    Obtiene todos los datos de los últimos 15 días de la estación "APPCR Muelle CC",
    organizados por variable para ser usados en gráficas.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Internal Server Error - Database connection failed"}), 500

    try:
        cur = conn.cursor()
        
        # Calcula el punto de inicio para la consulta (15 días atrás)
        quinze_dias_atras = datetime.utcnow() - timedelta(days=15)

        # Consulta que trae todos los datos de los sensores del muelle_cc de los últimos 15 días
        cur.execute("""
            SELECT 
                v.name AS variable_name,
                m.timestamp,
                m.value,
                u.symbol AS unit
            FROM oogsj_data.measurement m
            JOIN oogsj_data.sensor s ON s.id = m.sensor_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit u ON u.id = s.unit_id
            WHERE 
                s.name LIKE '%%160710%%'
                AND m.timestamp >= %s
            ORDER BY 
                v.name, m.timestamp;
        """, (quinze_dias_atras,))

        raw_data = cur.fetchall()
        cur.close()
        conn.close()

        # Procesa los datos para organizarlos en un formato amigable para gráficas
        data = {}
        for row in raw_data:
            variable_name, timestamp, value, unit = row
            if variable_name not in data:
                data[variable_name] = {
                    "unit": unit,
                    "data": []
                }
            data[variable_name]["data"].append({
                "timestamp": timestamp.isoformat(),
                "value": float(value)
            })
            
        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/muelle_cc/history: {e}")
        return jsonify({"error": "Internal Server Error"}), 500





#-----------------------------Endpoint prueba para ver datos erroneos-------------------------------------------------------------------------------
@app.route("/api/mediciones_negativas")
def mediciones_negativas():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.name, m.value, m.timestamp, u.symbol
            FROM oogsj_data.measurement m
            JOIN oogsj_data.sensor s ON m.sensor_id = s.id
            JOIN oogsj_data.unit u ON s.unit_id = u.id
            WHERE m.value < 0
            ORDER BY m.timestamp DESC;
        """)

        datos = [
            {
                "sensor": row[0],
                "valor": row[1],
                "timestamp": row[2].isoformat(),
                "unidad": row[3]
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()
        return jsonify(datos)

    except Exception as e:
        print(f"❌ ERROR en /api/mediciones_negativas: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

#--------------------- endpoints de papers para visualizarlos ---------------------

def parse_pagination():
    try:
        limit = max(1, min(int(request.args.get("limit", 10)), 100))
    except:
        limit = 10
    try:
        page = max(1, int(request.args.get("page", 1)))
    except:
        page = 1
    offset = (page - 1) * limit
    return limit, page, offset


@app.route("/api/library/list", methods=["GET"])
def library_list():
    # --- paginación segura ---
    limit, page, offset = parse_pagination()

    # --- orden permitido (whitelist) ---
    sort = (request.args.get("sort") or "year_desc").lower()
    order_by = {
        "year_desc":       "d.year DESC NULLS LAST, COALESCE(d.citations,0) DESC, d.title ASC",
        "year_asc":        "d.year ASC  NULLS FIRST, d.title ASC",
        "citations_desc":  "COALESCE(d.citations,0) DESC, d.year DESC NULLS LAST, d.title ASC",
        "citations_asc":   "COALESCE(d.citations,0) ASC,  d.year DESC NULLS LAST, d.title ASC",
        "title_asc":       "d.title ASC NULLS LAST"
    }.get(sort, "d.year DESC NULLS LAST, COALESCE(d.citations,0) DESC, d.title ASC")

    # --- SQL: total y página con autores + has_local_file ---
    sql_count = "SELECT COUNT(*) FROM oogsj_data.document;"

    sql_page = f"""
        SELECT
            d.id,
            d.title,
            d.year,
            d.venue,
            COALESCE(d.citations, 0) AS citations,
            d.url,
            d.doi,
            (d.storage_path IS NOT NULL) AS has_local_file,
            d.id AS canonical_id,            -- placeholder hasta que migremos duplicados
            FALSE AS is_duplicate,           -- idem
            COALESCE(
              json_agg(
                json_build_object('id', a.id, 'full_name', a.full_name)
                ORDER BY da.author_order
              ) FILTER (WHERE a.id IS NOT NULL),
              '[]'::json
            ) AS authors
        FROM oogsj_data.document d
        LEFT JOIN oogsj_data.document_author da ON da.document_id = d.id
        LEFT JOIN oogsj_data.author a          ON a.id = da.author_id
        GROUP BY d.id
        ORDER BY {order_by}
        LIMIT %s OFFSET %s;
    """

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute(sql_count)
        total = cur.fetchone()[0]

        cur.execute(sql_page, (limit, offset))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    # --- serialización ---
    items = []
    for r in rows:
        (
            doc_id, title, year, venue, citations,
            url, doi, has_local_file, canonical_id, is_duplicate, authors_json
        ) = r

        items.append({
            "id": doc_id,
            "title": title,
            "year": year,
            "venue": venue,
            "doi": doi,
            "url": url,
            "citations": citations,
            "authors": authors_json or [],
            "has_local_file": bool(has_local_file),
            "canonical_id": canonical_id,
            "is_duplicate": bool(is_duplicate),
        })

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "items": items
    })







@app.route("/api/library/search", methods=["GET"])
def library_search():
    q = (request.args.get("q") or "").strip()
    limit, page, offset = parse_pagination()

    base_where = "1=1"
    params = []
    if q:
        base_where = "(title ILIKE %s OR venue ILIKE %s OR doi ILIKE %s OR url ILIKE %s)"
        pat = f"%{q}%"; params = [pat, pat, pat, pat]

    sql_count = f"SELECT COUNT(*) FROM oogsj_data.document WHERE {base_where};"
    sql_page = f"""
        SELECT title, year, venue, COALESCE(citations,0) AS citations, url, doi
        FROM oogsj_data.document
        WHERE {base_where}
        ORDER BY year DESC NULLS LAST, COALESCE(citations,0) DESC, title
        LIMIT %s OFFSET %s;
    """

    conn = get_db_connection(); cur = conn.cursor()
    cur.execute(sql_count, params); total = cur.fetchone()[0]
    cur.execute(sql_page, params + [limit, offset]); rows = cur.fetchall()
    cur.close(); conn.close()

    items = [{
        "title": r[0], "year": r[1], "venue": r[2],
        "citations": r[3], "url": r[4], "doi": r[5]
    } for r in rows]

    return jsonify({"q": q, "page": page, "limit": limit, "total": total, "items": items})


@app.route("/api/library/<int:doc_id>", methods=["GET"])
def library_detail(doc_id: int):
    # Nota: seguimos aceptando el doc_id en la URL, pero no lo devolvemos en el JSON.
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("""
        SELECT title, year, venue, COALESCE(citations,0) AS citations, url, doi
        FROM oogsj_data.document
        WHERE id = %s
        LIMIT 1;
    """, (doc_id,))
    r = cur.fetchone()
    cur.close(); conn.close()

    if not r:
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "title": r[0], "year": r[1], "venue": r[2],
        "citations": r[3], "url": r[4], "doi": r[5]
    })


#--------------------------CRUD PAPERS-----------------------------------#

@app.route("/api/library/upload", methods=["POST"])
def library_upload():
    # --- validaciones básicas ---
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

    # campos opcionales
    year = request.form.get("year")
    venue = request.form.get("venue")
    doi = request.form.get("doi")
    url = request.form.get("url")
    abstract = request.form.get("abstract")
    authors_raw = (request.form.get("authors") or "").strip()
    # autores separados por ; o ,  -> lista limpia con orden
    authors = [a.strip() for chunk in authors_raw.split(";") for a in chunk.split(",") if a.strip()]
    # Si vinieron "Apellido, Nombre; Apellido, Nombre" no está mal; nos quedamos con el orden recibido.

    # --- guardar a disco ---
    base = secure_filename(title) or "document"
    f_uuid = uuid.uuid4().hex
    filename = f"{base}-{f_uuid}.pdf"
    dst_path = Path(app.config["UPLOAD_FOLDER"]) / filename
    file.save(dst_path)

    # Ruta “lógica” por si luego la servís con Nginx
    storage_path = str(dst_path)  # absoluta en el contenedor
    file_url = f"/files/{filename}"  # ver endpoint de files más abajo o servilo con Nginx

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        # --- insertar document ---
        cur.execute("""
            INSERT INTO oogsj_data.document (title, year, venue, citations, url, doi, storage_path)
            VALUES (%s, %s, %s, 0, %s, %s, %s)
            RETURNING id;
        """, (title, int(year) if (year and year.isdigit()) else None, venue or None, url or None, doi or None, storage_path))
        doc_id = cur.fetchone()[0]

        # --- autores (upsert por nombre) + relación con orden ---
        order_n = 1
        for full_name in authors:
            cur.execute("""
                INSERT INTO oogsj_data.author (full_name)
                VALUES (%s)
                ON CONFLICT (full_name) DO UPDATE SET full_name = EXCLUDED.full_name
                RETURNING id;
            """, (full_name,))
            author_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO oogsj_data.document_author (document_id, author_id, author_order)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (doc_id, author_id, order_n))
            order_n += 1

        # --- document_source ---
        cur.execute("""
            INSERT INTO oogsj_data.document_source (document_id, source_type, uploaded_by, source_name, raw_payload)
            VALUES (%s, 'user_upload', NULL, 'carga manual', %s);
        """, (doc_id, None))

        conn.commit()
        cur.close()

        return jsonify({
            "ok": True,
            "data": {
                "id": doc_id,
                "title": title,
                "year": int(year) if (year and year.isdigit()) else None,
                "venue": venue,
                "doi": doi,
                "url": url,
                "file_url": file_url
            }
        }), 201

    except Exception as e:
        conn.rollback()
        # si falló DB, borramos el archivo para no dejar basura
        try:
            dst_path.unlink(missing_ok=True)
        except Exception:
            pass
        print(f"❌ ERROR /api/library/upload: {e}")
        return jsonify({"ok": False, "error": "No se pudo guardar el documento"}), 500
    finally:
        conn.close()



@app.route("/api/library/admin/list", methods=["GET"])
def library_admin_list():
    limit, page, offset = parse_pagination()
    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("""
        SELECT id, title, year, venue, COALESCE(citations,0) AS citations, url, doi, storage_path, created_at
        FROM oogsj_data.document
        ORDER BY created_at DESC
        LIMIT %s OFFSET %s;
    """, (limit, offset))
    rows = cur.fetchall()
    cur.close(); conn.close()

    items = [{
        "id": r[0], "title": r[1], "year": r[2], "venue": r[3],
        "citations": r[4], "url": r[5], "doi": r[6],
        "storage_path": r[7], "created_at": r[8].isoformat() if r[8] else None
    } for r in rows]

    return jsonify({"page": page, "limit": limit, "items": items})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

