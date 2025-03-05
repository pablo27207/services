from flask import Flask, jsonify
from celery_tasks import fetch_mareograph
from services.logger_config import logger

app = Flask(__name__)

@app.route("/update/mareograph", methods=["POST"])
def update_mareograph():
    try:
        logger.info("📢 Recibida petición para actualizar datos del mareógrafo.")
        task = fetch_mareograph.delay()
        logger.info(f"🚀 Tarea de ingesta enviada. Task ID: {task.id}")
        return jsonify({"status": "Ingesta programada", "task_id": task.id}), 202
    except Exception as e:
        logger.error(f"❌ Error al enviar tarea: {str(e)}", exc_info=True)
        return jsonify({"error": "No se pudo programar la ingesta"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
