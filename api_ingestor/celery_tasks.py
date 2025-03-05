from celery import Celery
from celery.schedules import crontab
from services.mareograph import MareographScraper
from services.db_handler import DBHandler
from services.logger_config import logger

app = Celery('tasks', broker='redis://cache:6379/0', backend='redis://cache:6379/0')

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_mareograph(self):
    try:
        logger.info("📡 Ejecutando fetch_mareograph en Celery...")
        datos = MareographScraper.fetch_mareograph_data()

        if not datos:
            logger.warning("🚨 No se obtuvieron datos del scraping.")
            raise ValueError("Datos vacíos.")

        db = DBHandler()
        logger.info("💾 Insertando %d registros en la base de datos...", len(datos))
        db.insert_mareograph_data(datos)
        logger.info("✅ Datos insertados correctamente en la base de datos.")

        return {"status": "success", "records": len(datos)}

    except Exception as e:
        logger.error(f"⚠️ Error en la ingesta de datos: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60)

# ⏳ Configuración de Celery Beat para ejecutar cada 10 minutos
app.conf.beat_schedule = {
    'fetch_mareograph_every_10min': {
        'task': 'celery_tasks.fetch_mareograph',
        'schedule': crontab(minute='*/10'),
    },
}
app.conf.timezone = 'UTC'

# ⚙️ Configuraciones de reintento
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_reject_on_worker_lost = True
