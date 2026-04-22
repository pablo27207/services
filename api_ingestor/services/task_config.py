from celery.schedules import crontab

from services.mareograph_scraper       import MareographScraper
from services.buoy_scraper             import BuoyScraper
from services.tide_forecast_scraper    import TideScraper
from services.caleta_cordova_scraper   import WeatherCCScraper
from services.comodoro_rivadavia_scraper import WeatherCRScraper
from services.caleta_muelle_scraper    import WeatherCMScraper
from services.documentos_scraper       import ScientificDocScraper
from services.shn_avisos_scraper       import SHNAvisosScraper   # ← NUEVO

TASKS = {
    "buoy": {
        "scraper":  BuoyScraper.fetch_buoy_data,
        "schedule": crontab(minute=0),
    },
    "mareograph": {
        "scraper":  MareographScraper.fetch_mareograph_data,
        "schedule": crontab(minute="*/10"),
    },
    "tide_forecast": {
        "scraper":  TideScraper.fetch_tide_data,
        "schedule": crontab(minute=0, hour="*/6"),
    },
    "comodoro_rivadavia_port": {
        "scraper":  WeatherCRScraper.fetch_station_data,
        "schedule": crontab(minute="*/10"),
    },
    "caleta_muelle_dock": {
        "scraper":  WeatherCMScraper.fetch_station_data,
        "schedule": crontab(minute="*/10"),
    },
    "documentos_scraper": {
        "scraper":  ScientificDocScraper.fetch_data,
        "schedule": crontab(minute=17, hour=3),
    },
    "shn_avisos": {                                   # ← NUEVO
        "scraper":  SHNAvisosScraper.fetch_avisos_data,
        "schedule": crontab(minute=0),                # cada hora
    },
}