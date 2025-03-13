from celery.schedules import crontab
from services.mareograph_scraper import MareographScraper
from services.buoy_scraper import BuoyScraper
from services.tide_forecast_scraper import TideScraper

TASKS = {
    "buoy": {
        "scraper": BuoyScraper.fetch_buoy_data,
        "schedule": crontab(minute=0)  # Cada hora
    },
    "mareograph": {
        "scraper": MareographScraper.fetch_mareograph_data,
        "schedule": crontab(minute="*/10")  # Cada 10 min
    },
    "tide_forecast": {
        "scraper": TideScraper.fetch_tide_data,
        "schedule": crontab(minute=0, hour="*/6")  # Cada 6 horas
    }
}

# Para poder agregar un nuevo scraper hay que:
# 1. Crear un archivo en services/ con el nombre del scraper, ej: `services/<NOMBRE>_scraper.py` con un metodo fetch_<NOMBRE>_data
# 2. Agregar en este archivo el nuevo scraper con la siguiente estructura:
# "<NOMBRE>_scraper": {
#     "scraper": <NOMBRE>Scraper.fetch_<NOMBRE>_data,
#     "schedule": crontab(minute=0),  # Cada hora o el tiempo que se desee
# }
