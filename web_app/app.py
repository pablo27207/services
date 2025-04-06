from flask import Flask, jsonify, render_template, request
import psycopg2
import os
import math
import requests
import time
import hashlib

app = Flask(__name__)

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
    
    # Sensores de la boya CIDMAR-2
    sensor_ids = {
        3: "Altura de Olas",
        4: "Periodo de Olas",
        5: "Dirección de Olas",
        6: "Velocidad de Corriente",
        7: "Dirección de la Corriente",
        8: "Radiación PAR",
        9: "Batería"
    }

    cur.execute("""
        SELECT sensor_id, timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id IN (3, 4, 5, 6, 7, 8, 9)
        ORDER BY timestamp;
    """)

    raw_data = cur.fetchall()
    cur.close()
    conn.close()

    # Estructurar los datos agrupados por sensor
    data = {name: [] for name in sensor_ids.values()}
    for sensor_id, timestamp, value in raw_data:
        variable_name = sensor_ids.get(sensor_id, f"Sensor {sensor_id}")  # Por si falta alguno
        data[variable_name].append({"timestamp": timestamp, "value": value})

    return jsonify(data)



@app.route("/api/tide_forecast")
def get_tide_forecast_data():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id = 2
        ORDER BY timestamp;
    """)
    
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


#--------------------------------------------------------

#--------------------------------------------------------------------
@app.route("/api/weatherlink/debug")
def debug_signature():
    t = str(int(time.time()))
    signature = hashlib.sha256((WEATHERLINK_API_SECRET + t).encode("utf-8")).hexdigest()

    return jsonify({
        "t": t,
        "signature": signature,
        "url": f"https://api.weatherlink.com/v2/stations?api-key={WEATHERLINK_API_KEY}&t={t}&api-signature={signature}"
    })

#------------------------------------------------------------------------
@app.route("/api/weatherlink/puerto-comodoro")
def get_puerto_comodoro_data():
    try:
        api_key = "yz6qz7naojczuk6yvdtu5i1r3axhtbfb"
        api_secret = "kuxdheam0y0rcoimemr7dgszhiyteiqy"

        t = str(int(time.time()))
        signature = hashlib.sha256((api_secret + t).encode("utf-8")).hexdigest()

        # ❗ Aún falta definir el station_id real
        station_id = "REEMPLAZAR_ESTO"

        url = f"https://api.weatherlink.com/v2/current/{station_id}"
        params = {
            "api-key": api_key,
            "t": t,
            "api-signature": signature
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


#----------------------------------------------------------------
@app.route("/api/weatherlink/codova")
def get_caleta_cordova_data():
    try:
        api_key = "yl9c8tcwgmy3dccibgy4qvsi8igwzy0u"
        api_secret = "t5v6xlhg5b3qu5pzbijxm69kifxqgrlu"

        t = str(int(time.time()))
        signature = hashlib.sha256((api_secret + t).encode("utf-8")).hexdigest()

        # ❗ Aún falta definir el station_id real
        station_id = "REEMPLAZAR_ESTO"

        url = f"https://api.weatherlink.com/v2/current/{station_id}"
        params = {
            "api-key": api_key,
            "t": t,
            "api-signature": signature
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
