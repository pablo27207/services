from celery.schedules import crontab
from services.mareograph_scraper import MareographScraper
from services.buoy_scraper import BuoyScraper
from services.tide_forecast_scraper import TideScraper
from services.caleta_cordova_scraper import WeatherCCScraper
from services.comodoro_rivadavia_scraper import WeatherCRScraper
from services.caleta_muelle_scraper import WeatherCMScraper
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
    },
    #"caleta_cordova_dock": {
     #   "scraper": WeatherCCScraper.fetch_station_data,
      #  "schedule": crontab(minute="*/10")  # Cada 10 min
    #},
    "comodoro_rivadavia_port": {
        "scraper": WeatherCRScraper.fetch_station_data,
        "schedule": crontab(minute="*/10")  # Cada 10 min
    }
    
    ,
    #probando haciendolo de cero
    "caleta_muelle_dock": {
       "scraper": WeatherCMScraper.fetch_station_data,
       "schedule": crontab(minute="*/10")  # Cada 10 min
    }
}

# Para poder agregar un nuevo scraper hay que:
# 1. Crear un archivo en services/ con el nombre del scraper, ej: `services/<NOMBRE>_scraper.py` con un metodo fetch_<NOMBRE>_data
# 2. Agregar en este archivo el nuevo scraper con la siguiente estructura:
# "<NOMBRE>_scraper": {
#     "scraper": <NOMBRE>Scraper.fetch_<NOMBRE>_data,
#     "schedule": crontab(minute=0),  # Cada hora o el tiempo que se desee
# }
