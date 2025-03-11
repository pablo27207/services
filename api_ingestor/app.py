from flask import Flask, jsonify
from celery_tasks import app as celery_app
from services.logger_config import logger
from services.task_config import TASKS
from functools import partial

app = Flask(__name__)

# 📌 Función auxiliar para evitar sobrescribir la función en el bucle
def create_update_task(task_name):
    def update_task():
        try:
            logger.info(f"📢 Recibida petición para actualizar {task_name}.")
            task = celery_app.send_task(f"celery_tasks.fetch_{task_name}")
            logger.info(f"🚀 Tarea de ingesta enviada. Task ID: {task.id}")
            return jsonify({"status": "Ingesta programada", "task_id": task.id}), 202

        except Exception as e:
            logger.error(f"❌ Error al enviar tarea {task_name}: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500
    return update_task

# 📌 Crear dinámicamente los endpoints sin sobrescribir
for task_name in TASKS.keys():
    app.route(f"/update/{task_name}", methods=["POST"], endpoint=f"update_{task_name}")(create_update_task(task_name))
