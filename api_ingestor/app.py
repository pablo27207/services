from flask import Flask, jsonify
from celery_tasks import app as celery_app
from services.task_config import TASKS
from datetime import datetime
import redis
import psycopg2
import os

# Inicializa la aplicación Flask
app = Flask(__name__)

# Configuración de conexión a la base de datos
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",  # nombre del contenedor del servicio de base de datos en docker-compose
    "port": 5432
}

# Diccionario en memoria para registrar la última ejecución de cada tarea
LAST_RUNS = {task_name: None for task_name in TASKS.keys()}

@app.route("/status")
def status():
    estado = {
        "database": "ok",
        "celery": "ok",
        "redis": "ok",
        "last_runs": LAST_RUNS.copy()
    }

    # Verificar conexión a la base de datos
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")
        estado["database"] = "error"

    # Verificar conexión a Redis
    try:
        r = redis.Redis(host="cache", port=6379)
        r.ping()
    except Exception as e:
        print(f"❌ Error con Redis: {e}")
        estado["redis"] = "error"

    # Verificar Celery
    try:
        test_app = Celery('healthcheck', broker='redis://cache:6379/0')
        ping_response = test_app.control.ping(timeout=1)
        if not ping_response:
            raise Exception("No se recibió respuesta de Celery")
    except Exception as e:
        print(f"❌ Error con Celery: {e}")
        estado["celery"] = "error"

    return jsonify(estado)


# Registrar la hora de ejecución de una tarea
def registrar_ejecucion(task_name):
    LAST_RUNS[task_name] = datetime.utcnow().isoformat() + "Z"


# Generador de funciones para cada endpoint de actualización
def create_update_task(task_name):
    def update_task():
        try:
            print(f"📢 Recibida petición para actualizar '{task_name}'")
            task = celery_app.send_task(f"celery_tasks.fetch_{task_name}")
            print(f"🚀 Tarea enviada. ID: {task.id}")
            registrar_ejecucion(task_name)
            return jsonify({"status": "Ingesta programada", "task_id": task.id}), 202
        except Exception as e:
            print(f"❌ Error al enviar tarea '{task_name}': {e}")
            return jsonify({"error": str(e)}), 500
    return update_task


# Registrar dinámicamente las rutas de actualización
for task_name in TASKS.keys():
    app.route(f"/update/{task_name}", methods=["POST"], endpoint=f"update_{task_name}")(create_update_task(task_name))
