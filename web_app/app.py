
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

app = Flask(__name__)

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
        WHERE sensor_id = 1
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

STATION_ID = "160710"

@app.route("/api/weatherstation/puertoEstacionComodoro")
def get_weatherstation_puerto():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.name, m.timestamp, m.value, u.symbol
            FROM oogsj_data.sensor s
            JOIN oogsj_data.unit u ON s.unit_id = u.id
            JOIN oogsj_data.platform p ON s.platform_id = p.id
            JOIN LATERAL (
                SELECT timestamp, value
                FROM oogsj_data.measurement
                WHERE sensor_id = s.id
                ORDER BY timestamp DESC
                LIMIT 1
            ) m ON true
            WHERE p.id = 4  -- ID de la estación meteorológica Puerto CR
            ORDER BY s.name;
        """)

        data = [
            {
                "sensor": row[0],
                "timestamp": row[1].isoformat(),
                "value": float(row[2]),
                "unit": row[3]
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()
        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/weatherstation/puertoEstacionComodoro: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
#---------------------------Estacion Meteoroloigca Caleta Cordova Puerto --------------------------------------------------------------
@app.route("/api/weatherstation/puertoEstacionCaleta")
def get_weatherstation_puertoCaleta():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT s.name, m.timestamp, m.value, u.symbol
            FROM oogsj_data.sensor s
            JOIN oogsj_data.unit u ON s.unit_id = u.id
            JOIN oogsj_data.platform p ON s.platform_id = p.id
            JOIN LATERAL (
                SELECT timestamp, value
                FROM oogsj_data.measurement
                WHERE sensor_id = s.id
                ORDER BY timestamp DESC
                LIMIT 1
            ) m ON true
            WHERE p.id = 5  -- ID de la estación meteorológica Caleta Córdova
            ORDER BY s.name;
        """)

        data = [
            {
                "sensor": row[0],
                "timestamp": row[1].isoformat(),
                "value": float(row[2]),
                "unit": row[3]
            }
            for row in cur.fetchall()
        ]

        cur.close()
        conn.close()
        return jsonify(data)

    except Exception as e:
        print(f"❌ ERROR en /api/weatherstation/puertoEstacionCaleta: {e}")
        return jsonify({"error": "Internal Server Error"}), 500




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

