import logging
import io
from datetime import datetime
import os
from dotenv import load_dotenv

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
load_dotenv()  # Esto carga las variables desde .env

class WeatherCRScraper:
    API_KEY = os.getenv("API_KEY_PUERTO")
    API_SECRET = os.getenv("API_SECRET_PUERTO")
    STATION_ID = 160710
    LOCATION_ID = 1  # Reemplazar con el ID correspondiente
    PROCESSING_LEVEL_ID = 1  # Reemplazar si corresponde
    QUALITY_FLAG = 0  # Asumido como sin control de calidad aún


    @staticmethod
    def fetch_station_data():
        timestamp = int(time.time())
        url = f"https://api.weatherlink.com/v2/current/{cls.STATION_ID}/?t={timestamp}&api-key={cls.API_KEY}"
        headers = {
            "x-api-secret": cls.API_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(f"Error al obtener datos de Davis CR: {response.status_code}")
            return []

        data = response.json()
        results = []
        for sensor in data.get("sensors", []):
            for entry in sensor.get("data", []):
                ts = entry.get("ts")
                for key, sensor_id in cls.SENSOR_MAPPING.items():
                    value = entry.get(key)
                    if value is not None:
                        results.append((
                            datetime.fromtimestamp(ts, tz=timezone.utc),
                            value,
                            cls.QUALITY_FLAG,
                            cls.PROCESSING_LEVEL_ID,
                            sensor_id,
                            cls.LOCATION_ID
                        ))
        return results