from flask import Flask, jsonify
from celery_tasks import app as celery_app
from services.task_config import TASKS
from datetime import datetime
import redis
from celery import Celery
import psycopg2
import os

app = Flask(__name__)

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": 5432
}
# Diccionario en memoria de últimas ejecuciones
LAST_RUNS = {
    "buoy": None,
    "mareograph": None,
    "tide_forecast": None,
    "caleta_cordova_dock": None,
    "comodoro_rivadavia_port": None,
}
@app.route("/status")
def status():
    estado = {
        "database": "ok",
        "celery": "ok",
        "redis": "ok",
        "last_runs": LAST_RUNS.copy()
    }

    # Verificar conexión a base de datos
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        estado["database"] = "error"

    # Verificar Redis
    try:
        r = redis.Redis(host="cache", port=6379)
        r.ping()
    except Exception:
        estado["redis"] = "error"

    # Verificar Celery (mediante ping)
    try:
        celery_app = Celery('healthcheck', broker='redis://cache:6379/0')
        ping_response = celery_app.control.ping(timeout=1)
        if not ping_response:
            raise Exception("No response")
    except Exception:
        estado["celery"] = "error"

    return jsonify(estado)

def registrar_ejecucion(task_name):
    LAST_RUNS[task_name] = datetime.utcnow().isoformat() + "Z"

# 📌 Función auxiliar para evitar sobrescribir la función en el bucle
def create_update_task(task_name):
    def update_task():
        try:
            print(f"📢 Recibida petición para actualizar {task_name}.")
            task = celery_app.send_task(f"celery_tasks.fetch_{task_name}")
            print(f"🚀 Tarea de ingesta enviada. Task ID: {task.id}")
            registrar_ejecucion(task_name)
            return jsonify({"status": "Ingesta programada", "task_id": task.id}), 202

        except Exception as e:
            print(f"❌ Error al enviar tarea {task_name}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return update_task

# 📌 Crear dinámicamente los endpoints sin sobrescribir
for task_name in TASKS.keys():
    app.route(f"/update/{task_name}", methods=["POST"], endpoint=f"update_{task_name}")(create_update_task(task_name))
