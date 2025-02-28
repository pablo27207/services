from flask import Flask, jsonify
from celery_tasks import fetch_mareograph

app = Flask(__name__)

@app.route("/update/mareograph", methods=["POST"])
def update_mareograph():
    task = fetch_mareograph.delay()
    return jsonify({"status": "Ingesta programada", "task_id": task.id}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
