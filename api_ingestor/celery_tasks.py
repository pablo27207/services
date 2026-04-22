from celery import Celery
from services.db_handler import DBHandler
from services.task_config import TASKS

app = Celery('tasks', broker='redis://cache:6379/0', backend='redis://cache:6379/0')

# Tareas que usan insert_avisos en lugar de insert_measurements
AVISOS_TASKS = {"shn_avisos"}

def create_celery_task(task_name, scraper):
    @app.task(bind=True, name=f"celery_tasks.fetch_{task_name}",
              max_retries=3, default_retry_delay=60)
    def task(self):
        try:
            print(f"🚀 Ejecutando {task_name}...")
            datos = scraper()
            if not datos:
                print(f"🚨 Sin datos para {task_name}.")
                raise ValueError("Datos vacíos.")

            db = DBHandler()
            print(f"💾 Insertando {len(datos)} registros para {task_name}...")

            if task_name in AVISOS_TASKS:
                db.insert_avisos(datos)
            else:
                db.insert_measurements(datos)

            print(f"✅ {task_name} completado.")
            return {"status": "success", "records": len(datos)}

        except Exception as e:
            print(f"⚠️ Error en {task_name}: {e}")
            raise self.retry(exc=e, countdown=60)

    return task

for task_name, config in TASKS.items():
    create_celery_task(task_name, config["scraper"])

app.conf.beat_schedule = {
    task_name: {
        "task":     f"celery_tasks.fetch_{task_name}",
        "schedule": config["schedule"],
    }
    for task_name, config in TASKS.items()
}
app.conf.timezone                   = 'UTC'
app.conf.task_acks_late             = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_reject_on_worker_lost = True
app.conf.worker_concurrency         = 4