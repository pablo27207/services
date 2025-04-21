import io
from datetime import datetime
import os
from .config import get_env_var


class WeatherCCScraper:
    API_KEY = get_env_var("API_KEY_MUELLE")
    API_SECRET = get_env_var("API_SECRET_MUELLE")
    STATION_ID = 160710
    LOCATION_ID = 1  # Reemplazar con el ID correspondiente
    PROCESSING_LEVEL_ID = 1  # Reemplazar si corresponde
    QUALITY_FLAG = 0  # Asumido como sin control de calidad aún


    @staticmethod
    def fetch_station_data():
        results= []
        return results