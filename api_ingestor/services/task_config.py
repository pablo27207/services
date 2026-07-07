from celery.schedules import crontab

from services.mareograph_scraper       import MareographScraper
from services.buoy_scraper             import BuoyScraper
from services.tide_forecast_scraper    import TideScraper
from services.caleta_cordova_scraper   import WeatherCCScraper
from services.comodoro_rivadavia_scraper import WeatherCRScraper
from services.caleta_muelle_scraper    import WeatherCMScraper
from services.documentos_scraper       import ScientificDocScraper
from services.shn_avisos_scraper       import SHNAvisosScraper
from services.emac_cmd0_scraper        import EMACCMD0Scraper     # ← Estación CMD0 Caleta Córdova
from services.emac_cmd1_scraper        import EMACCMD1Scraper     # ← Estación CMD1

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
    "shn_avisos": {
        "scraper":  SHNAvisosScraper.fetch_avisos_data,
        "schedule": crontab(minute=0),                # cada hora
    },
    # Estación hidrometeorológica EMAC CMD0 – Caleta Córdova
    # La API EMAC entrega histórico de 30 días; consultar cada 30 min
    # equilibra frescura de datos con carga sobre el servidor EMAC.
    "emac_cmd0_station": {
        "scraper":  EMACCMD0Scraper.fetch_station_data,
        "schedule": crontab(minute="*/30"),           # cada 30 minutos
    },
    # Estación hidrometeorológica EMAC CMD1
    "emac_cmd1_station": {
        "scraper":  EMACCMD1Scraper.fetch_station_data,
        "schedule": crontab(minute="*/30"),           # cada 30 minutos
    },
}