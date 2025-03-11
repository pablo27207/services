from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from services.mareograph import MareographScraper
from services.buoy import BuoyScraper
from services.tide_forecast import TideScraper
from services.db_handler import DBHandler
from services.logger_config import logger

app = Celery('tasks', broker='redis://cache:6379/0', backend='redis://cache:6379/0')

@app.task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_buoy_data(self):
    try:
        logger.info("🌊 Ejecutando fetch_buoy_data en Celery...")
        datos = BuoyScraper.fetch_buoy_data()

        if not datos:
            logger.warning("🚨 No se obtuvieron datos de la boya.")
            raise ValueError("Datos vacíos.")

        db = DBHandler()
        logger.info("💾 Insertando %d registros en la base de datos...", len(datos))
        db.insert_buoy_data(datos)
        logger.info("✅ Datos de la boya insertados correctamente.")

        return {"status": "success", "records": len(datos)}

    except Exception as e:
        logger.error(f"⚠️ Error en la ingesta de datos de la boya: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_mareograph(self):
    try:
        logger.info("📡 Ejecutando fetch_mareograph en Celery...")
        datos = MareographScraper.fetch_mareograph_data()
        if not datos:
            logger.warning("🚨 No se obtuvieron datos del scraping de mareograph.")
            raise ValueError("Datos vacíos.")
        db = DBHandler()
        logger.info("💾 Insertando %d registros en la base de datos...", len(datos))
        db.insert_mareograph_data(datos)
        logger.info("✅ Datos insertados correctamente en la base de datos.")
        return {"status": "success", "records": len(datos)}
    except Exception as e:
        logger.error(f"⚠️ Error en la ingesta de datos: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60)
    
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_tide_forecast(self):
    try:
        logger.info("🌊 Iniciando la recolección de datos de mareas estimadas...")
        # Obtener los datos
        datos = TideScraper.fetch_tide_data()
        if not datos:
            logger.warning("🚨 No se obtuvieron datos del scraping de hidrografía.")
            raise ValueError("Datos vacíos.")
        # Insertar en la base de datos
        db = DBHandler()
        logger.info(f"💾 Insertando {len(datos)} registros en la base de datos...")
        db.insert_tide_forecast(datos)
        logger.info("✅ Datos insertados correctamente en la base de datos.")
        return {"status": "success", "records": len(datos)}

    except Exception as e:
        logger.error(f"⚠️ Error en la ingesta de datos: {e}", exc_info=True)
        raise self.retry(exc=e, countdown=60)
    
# ⏳ Configuración de Celery Beat para ejecutar con regularidad
app.conf.beat_schedule = {
    'fetch_mareograph_every_10min': {
        'task': 'celery_tasks.fetch_mareograph',
        'schedule': crontab(minute='*/10'),
    },
    'fetch_buoy_every_60min': {
        'task': 'celery_tasks.fetch_buoy_data',
        'schedule': crontab(minute='0'), # Se ejecuta en el minuto 0 de cada hora
    },
    "fetch_tide_forecast_every_6_hours": {
        "task": "celery_tasks.fetch_tide_forecast",
        "schedule": crontab(minute=0, hour="*/6"),  # Cada 6 horas
    }
}
app.conf.timezone = 'UTC'

# ⚙️ Configuraciones de reintento
app.conf.task_acks_late = True
app.conf.worker_prefetch_multiplier = 1
app.conf.task_reject_on_worker_lost = True
