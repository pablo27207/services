
#----------Con esto debo hacer mi backend ---------------------------------------------#
from flask import Flask, jsonify, render_template, request, send_file, send_from_directory, abort, make_response
import os, math, re, uuid
from datetime import datetime, timedelta
from pathlib import Path
import psycopg2
import jwt
from passlib.hash import bcrypt
from functools import wraps
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message




app = Flask(__name__)

# === AUTH/JWT (debe ir antes de cualquier @admin_required) ===
JWT_SECRET = os.getenv("JWT_SECRET", "cambia-esta-clave")
JWT_ISS = "oogsj-auth"
JWT_EXP_MIN = 120
SECURE_COOKIES = os.getenv("SECURE_COOKIES", "false").lower() == "true"

def _create_jwt(payload: dict):
    now = datetime.utcnow()
    to_encode = {"iss": JWT_ISS, "iat": now, "exp": now + timedelta(minutes=JWT_EXP_MIN), **payload}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

def _decode_jwt(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer=JWT_ISS)

def _cookie_opts():
    return dict(httponly=True, secure=SECURE_COOKIES, samesite="Lax", path="/")

def current_user():
    tok = request.cookies.get("auth_token")
    if not tok:
        return None
    try:
        data = _decode_jwt(tok)
        return {
            "id": data.get("uid"),
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "is_admin": bool(data.get("is_admin")),
        }
    except Exception:
        return None

def admin_required(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        u = current_user()
        if not u or not u["is_admin"]:
            return jsonify({"error": "No autorizado"}), 401
        return fn(*args, **kwargs)
    return _wrap
# === FIN AUTH/JWT ===






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

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS','true').lower()=='true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])


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

    cur = None
    try:
        cur = conn.cursor()

        # Trae el último dato por sensor SOLO de la plataforma indicada.
        # Usamos INNER JOIN LATERAL (JOIN ... ON TRUE) para excluir sensores sin mediciones.
        cur.execute("""
            SELECT
                s.id   AS sensor_id,
                s.name AS sensor,
                v.name AS variable,
                u.symbol AS unit,
                m."timestamp" AS ts,
                m.value AS val
            FROM oogsj_data.platform p
            JOIN oogsj_data.sensor   s ON s.platform_id = p.id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            JOIN LATERAL (
                SELECT m2."timestamp", m2.value
                FROM oogsj_data.measurement m2
                WHERE m2.sensor_id = s.id
                ORDER BY m2."timestamp" DESC
                LIMIT 1
            ) m ON TRUE
            WHERE p.name = %s
            ORDER BY v.name, s.name;
        """, ("APPCR Puerto CR",))

        rows = cur.fetchall()

        data = [
            {
                "sensor_id": r[0],
                "sensor": r[1],
                "variable": r[2],
                "unit": r[3],
                "timestamp": r[4].isoformat() if r[4] else None,
                "value": float(r[5]) if r[5] is not None else None,
            }
            for r in rows
        ]

        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/puerto: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass
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

    cur = None
    try:
        cur = conn.cursor()

        diez_dias_atras = datetime.utcnow() - timedelta(days=10)

        cur.execute("""
            SELECT 
                v.name        AS variable_name,
                u.symbol      AS unit,
                m."timestamp" AS ts,
                m.value       AS val
            FROM oogsj_data.measurement m
            JOIN oogsj_data.sensor   s ON s.id = m.sensor_id
            JOIN oogsj_data.platform p ON p.id = s.platform_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            WHERE p.name = %s
              AND m."timestamp" >= %s
            ORDER BY v.name, m."timestamp";
        """, ("APPCR Puerto CR", diez_dias_atras))

        rows = cur.fetchall()

        data = {}
        for variable_name, unit, ts, val in rows:
            if variable_name not in data:
                data[variable_name] = {
                    "unit": unit,
                    "data": []
                }

            data[variable_name]["data"].append({
                "timestamp": ts.isoformat() if ts else None,
                "value": float(val) if val is not None else None
            })

        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/puerto/history: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass

#--------------------------endpoint estacion meteorologica caleta cordova ultimos datos ----------------------------------------------------
### ESTE ES EL CORRECTO, LUEGO VER QUE METODOS SOBRAN Y COMENTARLO

from flask import jsonify
from datetime import timezone

@app.route("/api/appcr/muelle_cc", methods=["GET"])
def get_muelle_cc_data():
    """
    Obtiene el último registro de cada sensor de la estación APPCR Muelle CC
    y lo normaliza a un formato internacional consumible.
    """
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Internal Server Error - Database connection failed"}), 500

    cur = None
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                s.id   AS sensor_id,
                s.name AS sensor,
                v.name AS variable,
                u.symbol AS unit,
                m."timestamp" AS ts,
                m.value AS val
            FROM oogsj_data.platform p
            JOIN oogsj_data.sensor   s ON s.platform_id = p.id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN LATERAL (
                SELECT m2."timestamp", m2.value
                FROM oogsj_data.measurement m2
                WHERE m2.sensor_id = s.id
                ORDER BY m2."timestamp" DESC
                LIMIT 1
            ) m ON TRUE
            WHERE p.name = %s
            ORDER BY v.name, s.name;
        """, ("APPCR Muelle CC",))

        rows = cur.fetchall()

        # Diccionario de normalización por variable
        # source_unit = unidad esperada del dato crudo
        # target_unit = unidad final internacional
        VARIABLE_MAP = {
            "Bar": {
                "key": "barometric_pressure",
                "label": "Presión barométrica",
                "source_unit": "hPa",
                "target_unit": "hPa"
            },
            "Dew Point Out": {
                "key": "dew_point_outdoor",
                "label": "Punto de rocío exterior",
                "source_unit": "°F",
                "target_unit": "°C"
            },
            "Heat Index Out": {
                "key": "heat_index_outdoor",
                "label": "Índice de calor exterior",
                "source_unit": "°F",
                "target_unit": "°C"
            },
            "Rainfall Clicks": {
                "key": "rainfall",
                "label": "Precipitación",
                "source_unit": "clicks",
                "target_unit": "mm"
            },
            "Temp In": {
                "key": "indoor_temperature",
                "label": "Temperatura interior",
                "source_unit": "°F",
                "target_unit": "°C"
            },
            "Temp Out": {
                "key": "outdoor_temperature",
                "label": "Temperatura exterior",
                "source_unit": "°F",
                "target_unit": "°C"
            },
            "Wind Chill": {
                "key": "wind_chill",
                "label": "Sensación térmica por viento",
                "source_unit": "°F",
                "target_unit": "°C"
            },
            "Wind Dir Of Prevail": {
                "key": "wind_direction",
                "label": "Dirección predominante del viento",
                "source_unit": "degrees",
                "target_unit": "degrees"
            },
            "Wind Speed Avg": {
                "key": "wind_speed_avg",
                "label": "Velocidad media del viento",
                "source_unit": "mph",
                "target_unit": "m/s"
            }
        }

        def fahrenheit_to_celsius(value):
            return (value - 32) * 5.0 / 9.0

        def mph_to_ms(value):
            return value * 0.44704

        def identity(value):
            return value

        def clicks_to_mm(value):
            # AJUSTAR según la estación/sensor real de WeatherLink
            # Esto es un placeholder razonable solo si sabés cuántos mm vale cada click.
            MM_PER_CLICK = 0.2
            return value * MM_PER_CLICK

        def convert_value(variable_name, raw_value):
            if raw_value is None:
                return None, None

            config = VARIABLE_MAP.get(variable_name)
            if not config:
                return raw_value, None

            source_unit = config["source_unit"]
            target_unit = config["target_unit"]

            if source_unit == target_unit:
                return round(identity(raw_value), 2), target_unit

            if source_unit == "°F" and target_unit == "°C":
                return round(fahrenheit_to_celsius(raw_value), 2), target_unit

            if source_unit == "mph" and target_unit == "m/s":
                return round(mph_to_ms(raw_value), 2), target_unit

            if source_unit == "clicks" and target_unit == "mm":
                return round(clicks_to_mm(raw_value), 2), target_unit

            if source_unit == "degrees" and target_unit == "degrees":
                return round(raw_value, 2), "°"

            return round(raw_value, 2), target_unit

        def normalize_timestamp(ts):
            if ts is None:
                return None
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

        variables = {}
        latest_timestamp = None

        for r in rows:
            sensor_id = r[0]
            sensor_name = r[1]
            variable_name = r[2]
            db_unit = r[3]
            ts = r[4]
            raw_value = float(r[5]) if r[5] is not None else None

            config = VARIABLE_MAP.get(variable_name)

            # Si no está mapeada, la dejamos en formato fallback
            if config:
                converted_value, final_unit = convert_value(variable_name, raw_value)
                key = config["key"]
                label = config["label"]
            else:
                converted_value = round(raw_value, 2) if raw_value is not None else None
                final_unit = db_unit
                key = variable_name.lower().replace(" ", "_")
                label = variable_name

            iso_ts = normalize_timestamp(ts)

            if latest_timestamp is None and iso_ts is not None:
                latest_timestamp = iso_ts

            variables[key] = {
                "label": label,
                "sensor": sensor_name,
                "sensor_id": sensor_id,
                "value": converted_value,
                "unit": final_unit,
                "timestamp": iso_ts
            }

        response = {
            "station_name": "APPCR Muelle CC",
            "station_code": "appcr_muelle_cc",
            "timestamp": latest_timestamp,
            "variables": variables
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"❌ ERROR en /api/appcr/muelle_cc: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    finally:
        try:
            if cur:
                cur.close()
        except Exception:
            pass
        try:
            if conn:
                conn.close()
        except Exception:
            pass
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

    # --- filtros opcionales ---
    year_min = request.args.get("year_min")
    year_max = request.args.get("year_max")
    has_doi  = request.args.get("has_doi")   # "true"/"false"/None
    has_file = request.args.get("has_file")  # "true"/"false"/None

    # --- orden permitido (whitelist), igual a /list ---
    sort = (request.args.get("sort") or "year_desc").lower()
    sort_map = {
        "year_desc":       "d.year DESC NULLS LAST, COALESCE(d.citations,0) DESC, d.title ASC",
        "year_asc":        "d.year ASC NULLS FIRST, d.title ASC",
        "citations_desc":  "COALESCE(d.citations,0) DESC, d.year DESC NULLS LAST, d.title ASC",
        "citations_asc":   "COALESCE(d.citations,0) ASC,  d.year DESC NULLS LAST, d.title ASC",
        "title_asc":       "d.title ASC NULLS LAST"
    }
    base_order = sort_map.get(sort, sort_map["year_desc"])

    # --- heurística: si q "parece" DOI, priorizar match exacto por DOI ---
    looks_like_doi = bool(re.match(r"^\s*10\.\S+$", q)) if q else False
    relevance_order = ""
    doi_exact_param = None
    if q and looks_like_doi:
        relevance_order = "CASE WHEN lower(d.doi) = lower(%s) THEN 0 ELSE 1 END, "
        doi_exact_param = q

    # --- WHERE dinámico con joins a autores ---
    where_parts = ["1=1"]
    params = []

    if q:
        # busco en title/venue/url/doi y también en autor
        where_parts.append("("
            "d.title ILIKE %s OR "
            "d.venue ILIKE %s OR "
            "d.doi   ILIKE %s OR "
            "d.url   ILIKE %s OR "
            "a.full_name ILIKE %s"
        ")")
        pat = f"%{q}%"
        params.extend([pat, pat, pat, pat, pat])

    if year_min and year_min.isdigit():
        where_parts.append("d.year >= %s")
        params.append(int(year_min))

    if year_max and year_max.isdigit():
        where_parts.append("d.year <= %s")
        params.append(int(year_max))

    if has_doi in ("true", "false"):
        where_parts.append("d.doi IS NOT NULL" if has_doi == "true" else "d.doi IS NULL")

    if has_file in ("true", "false"):
        where_parts.append("(d.storage_path IS NOT NULL)" if has_file == "true" else "(d.storage_path IS NULL)")

    where_sql = " AND ".join(where_parts)

    # --- COUNT con DISTINCT porque hay join a autores ---
    sql_count = f"""
        SELECT COUNT(DISTINCT d.id)
        FROM oogsj_data.document d
        LEFT JOIN oogsj_data.document_author da ON da.document_id = d.id
        LEFT JOIN oogsj_data.author a          ON a.id = da.author_id
        WHERE {where_sql};
    """

    # --- página con autores (json_agg) y has_local_file ---
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
            d.id AS canonical_id,               -- placeholder hasta migrar duplicados
            FALSE AS is_duplicate,              -- idem
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
        WHERE {where_sql}
        GROUP BY d.id
        ORDER BY {relevance_order}{base_order}
        LIMIT %s OFFSET %s;
    """

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        # total
        cur.execute(sql_count, params)
        total = cur.fetchone()[0]

        # página (si hay boost por DOI exacto, ese param va primero)
        page_params = list(params)
        if relevance_order:
            page_params.append(doi_exact_param)
        page_params.extend([limit, offset])

        cur.execute(sql_page, page_params)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    # --- serialización ---
    items = []
    for (
        doc_id, title, year, venue, citations, url, doi,
        has_local_file, canonical_id, is_duplicate, authors_json
    ) in rows:
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
        "q": q,
        "page": page,
        "limit": limit,
        "total": total,
        "items": items
    })



#ojo con estoooo
@app.route("/api/library/<int:doc_id>", methods=["GET"])
def library_detail(doc_id: int):
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        # Documento + autores (ordenados)
        cur.execute("""
            SELECT
                d.id,
                d.title,
                d.year,
                d.venue,
                COALESCE(d.citations, 0) AS citations,
                d.url,
                d.doi,
                d.storage_path,
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
            WHERE d.id = %s
            GROUP BY d.id;
        """, (doc_id,))
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "not found"}), 404

    (r_id, title, year, venue, citations, url, doi, storage_path, authors_json) = row
    has_local_file = bool(storage_path)

    data = {
        "id": r_id,
        "title": title,
        "year": year,
        "venue": venue,
        "doi": doi,
        "url": url,
        "citations": citations,
        "authors": authors_json or [],
        "has_local_file": has_local_file,
        "download_url": f"/api/library/file/{r_id}" if has_local_file else None,
        # placeholders hasta migrar duplicados
        "canonical_id": r_id,
        "is_duplicate": False
    }
    return jsonify(data)



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


@app.route("/api/library/file/<int:doc_id>", methods=["GET"])
def library_file_download(doc_id: int):
    # (si tenés auth/roles, validalo acá antes de servir)
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT storage_path, title
            FROM oogsj_data.document
            WHERE id = %s
            LIMIT 1;
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

    # Seguridad: la ruta debe vivir dentro de UPLOAD_FOLDER
    uploads_root = Path(app.config["UPLOAD_FOLDER"]).resolve()
    file_path    = Path(storage_path).resolve()

    try:
        file_path.relative_to(uploads_root)
    except Exception:
        # Ruta fuera de uploads => bloquear
        return jsonify({"error": "forbidden_path"}), 403

    if not file_path.exists():
        return jsonify({"error": "file_missing"}), 404

    # Nombre de descarga prolijo
    base_name = secure_filename(title or "document")
    download_name = f"{base_name}.pdf"

    # Sirve como attachment
    return send_file(
        str(file_path),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=download_name,
        max_age=3600  # cache 1h si querés
    )








#--------------------------CRUD PAPERS-----------------------------------#

@app.route("/api/library/upload", methods=["POST"])
@admin_required
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
@admin_required
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


#---------------login del administrador , iniciar sesion, dashboard ------------------------------#
JWT_SECRET = os.getenv("JWT_SECRET", "cambia-esta-clave")
JWT_ISS = "oogsj-auth"
JWT_EXP_MIN = 120  # 2 horas


def _create_jwt(payload: dict):
    now = datetime.utcnow()
    to_encode = {"iss": JWT_ISS, "iat": now, "exp": now + timedelta(minutes=JWT_EXP_MIN), **payload}
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")


def _decode_jwt(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer=JWT_ISS)


SECURE_COOKIES = os.getenv("SECURE_COOKIES", "false").lower() == "true"

def _cookie_opts():
    return dict(httponly=True, secure=SECURE_COOKIES, samesite="Lax", path="/")



def current_user():
    tok = request.cookies.get("auth_token")
    if not tok:
        return None
    try:
        data = _decode_jwt(tok)
        return {
            "id": data.get("uid"),
            "email": data.get("email"),
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "is_admin": bool(data.get("is_admin"))
        }
    except Exception:
        return None


def admin_required(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        u = current_user()
        if not u or not u["is_admin"]:
            return jsonify({"error": "No autorizado"}), 401
        return fn(*args, **kwargs)
    return _wrap

#--------------------endpoints auth-----------------
@app.post("/api/auth/login")
def auth_login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return jsonify({"error": "Credenciales inválidas"}), 400

    conn = get_db_connection(); cur = conn.cursor()
    cur.execute("""
      SELECT id, first_name, last_name, email, COALESCE(password_hash,''), COALESCE(is_admin,false)
      FROM oogsj_data."user"
      WHERE LOWER(email)=LOWER(%s)
    """, (email,))
    row = cur.fetchone()
    cur.close(); conn.close()

    if not row or not row[4] or not bcrypt.verify(password, row[4]):
        return jsonify({"error":"Email o contraseña incorrectos"}), 401

    token = _create_jwt({
        "uid": row[0], "email": row[3],
        "first_name": row[1], "last_name": row[2],
        "is_admin": row[5]
    })
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("auth_token", token, **_cookie_opts())
    return resp


@app.post("/api/auth/logout")
def auth_logout():
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("auth_token", "", expires=0, **_cookie_opts())
    return resp


@app.get("/api/auth/me")
def auth_me():
    u = current_user()
    if not u:
        return jsonify({"authenticated": False}), 200
    return jsonify({"authenticated": True, "user": u}), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

