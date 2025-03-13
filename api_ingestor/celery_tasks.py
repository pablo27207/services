from celery import Celery
from services.db_handler import DBHandler
from services.logger_config import logger
from services.task_config import TASKS

app = Celery('tasks', broker='redis://cache:6379/0', backend='redis://cache:6379/0')

def create_celery_task(task_name, scraper):
    """Crea y registra dinámicamente una tarea de Celery."""
    @app.task(bind=True, name=f"celery_tasks.fetch_{task_name}", max_retries=3, default_retry_delay=60)
    def task(self):
        try:
            logger.info(f"🚀 Ejecutando {task_name} en Celery...")
            datos = scraper()
            if not datos:
                logger.warning(f"🚨 No se obtuvieron datos para {task_name}.")
                raise ValueError("Datos vacíos.")

            db = DBHandler()
            logger.info(f"💾 Insertando {len(datos)} registros en la base de datos para {task_name}...")
            db.insert_measurements(datos)
            logger.info(f"✅ Datos insertados correctamente para {task_name}.")
            return {"status": "success", "records": len(datos)}

        except Exception as e:
            logger.error(f"⚠️ Error en la ingesta de datos para {task_name}: {e}", exc_info=True)
            raise self.retry(exc=e, countdown=60)
    
    return task

# 📌 Crear todas las tareas dinámicamente
for task_name, config in TASKS.items():
    create_celery_task(task_name, config["scraper"])  # Eliminado db_insert

# ⏳ Configuración de Celery Beat
app.conf.beat_schedule = {
    task_name: {
        "task": f"celery_tasks.fetch_{task_name}",  # Genera automáticamente el nombre de la tarea
        "schedule": config["schedule"]
    }
    for task_name, config in TASKS.items()
}
app.conf.timezone = 'UTC'
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_reject_on_worker_lost = True
app.conf.worker_concurrency = 4  # Ajusta según tu capacidad de procesamiento
