from flask import Flask, jsonify
from celery_tasks import app as celery_app
from services.task_config import TASKS

app = Flask(__name__)

# 📌 Función auxiliar para evitar sobrescribir la función en el bucle
def create_update_task(task_name):
    def update_task():
        try:
            print(f"📢 Recibida petición para actualizar {task_name}.")
            task = celery_app.send_task(f"celery_tasks.fetch_{task_name}")
            print(f"🚀 Tarea de ingesta enviada. Task ID: {task.id}")
            return jsonify({"status": "Ingesta programada", "task_id": task.id}), 202

        except Exception as e:
            print(f"❌ Error al enviar tarea {task_name}: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return update_task

# 📌 Crear dinámicamente los endpoints sin sobrescribir
for task_name in TASKS.keys():
    app.route(f"/update/{task_name}", methods=["POST"], endpoint=f"update_{task_name}")(create_update_task(task_name))
