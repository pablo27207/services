from flask import Flask, jsonify, render_template, request
import psycopg2
import os

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
    
    # Obtener los datos del sensor del mareógrafo
    cur.execute("""
        SELECT timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id = 1
        ORDER BY timestamp;
    """)
    
    data = [{"timestamp": row[0], "level": float(row[1]) if row[1] is not None else 0.0} for row in cur.fetchall()]
    
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
    
    # Obtener datos del sensor del modelo de predicción de mareas
    cur.execute("""
        SELECT timestamp, value
        FROM oogsj_data.measurement
        WHERE sensor_id = 2
        ORDER BY timestamp;
    """)
    
    data = [{"timestamp": row[0], "level": float(row[1]) if row[1] is not None else 0.0} for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    return jsonify(data)


    #-------------------------------------------Ultimo endpoit los ultimos datos sensados de la boya 
@app.route("/api/buoy/latest")
def get_latest_buoy_data():
    conn = get_db_connection()
    cur = conn.cursor()

        # Consulta para obtener el último valor sensado de cada sensor de la boya CIDMAR-2
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
            s.platform_id = 3  -- ID de la boya CIDMAR-2
        ORDER BY
            m.sensor_id, m.timestamp DESC;
        """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Estructura del JSON
    data = {}
    for name, timestamp, value, unit in rows:
            data[name] = {
            "timestamp": timestamp,
            "value": float(value) if value is not None else None,
            "unit": unit
            }

    return jsonify(data)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
