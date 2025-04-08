import logging
import io
from datetime import datetime

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class WeatherCCScraper:
    @staticmethod
    def fetch_station_data():
    
        return results  # Devuelve lista de tuplas [(timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)]
