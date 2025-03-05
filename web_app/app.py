from flask import Flask, jsonify, render_template
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
    cur.execute("SELECT timestamp, level FROM mareograph_data ORDER BY timestamp;")
    data = [{"timestamp": row[0], "level": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
