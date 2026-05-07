from celery import Celery
from celery.schedules import crontab
from services.db_handler import DBHandler
from services.task_config import TASKS
from services.csv_export_service import CSVExportService

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

@app.task(bind=True, name="celery_tasks.monthly_csv_export",
          max_retries=2, default_retry_delay=300)
def monthly_csv_export(self, year: int = None, month: int = None):
    try:
        results = CSVExportService.generate_all_platforms(year=year, month=month)
        return {"status": "success", "files_generated": len(results), "paths": results}
    except Exception as exc:
        print(f"❌ Error en exportación mensual: {exc}")
        raise self.retry(exc=exc, countdown=300)

app.conf.beat_schedule["monthly_csv_export"] = {
    "task":     "celery_tasks.monthly_csv_export",
    "schedule": crontab(minute=0, hour=0, day_of_month=1),
}


@app.task(bind=True, name="celery_tasks.backfill_all_exports",
          max_retries=1, default_retry_delay=600,
          soft_time_limit=10800, time_limit=12600)
def backfill_all_exports(self, start_year: int = None, start_month: int = None):
    """Genera CSV y TXT históricos para todas las plataformas desde el inicio de los datos."""
    try:
        results = CSVExportService.backfill_all_months(
            start_year=start_year, start_month=start_month
        )
        return {"status": "success", "files_generated": len(results), "paths": results}
    except Exception as exc:
        print(f"❌ Error en backfill: {exc}")
        raise self.retry(exc=exc, countdown=600)

app.conf.timezone                   = 'UTC'
app.conf.task_acks_late             = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_reject_on_worker_lost = True
app.conf.worker_concurrency         = 4