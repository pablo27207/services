import requests
import logging
import pandas as pd
import io
from datetime import datetime

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BuoyScraper:
    BASE_URL = "http://emac.criba.edu.ar/servicios/getHistoryValues.php"
    STATION_CODE = "EACC"
    
    # Mapeo de códigos de variable a IDs de sensores en la base de datos
    VARIABLES = {
        "14": 3,  # Sensor de Altura de Olas
        "15": 4,  # Sensor de Periodo de Olas
        "32": 5,  # Sensor de Dirección de Olas
        "23": 6,  # Sensor de Velocidad de Corriente
        "29": 7,  # Sensor de Dirección de la Corriente
        "33": 8,  # Sensor de Radiación PAR
        "08": 9   # Sensor de Batería
    }

    @staticmethod
    def fetch_buoy_data():
        results = []
        quality_flag = 1  # Se asume que los datos de la boya son no chqueados
        processing_level_id = 1  # Raw data
        location_id = 2  # ID de la ubicación de la boya CIDMAR-2

        for var_code, sensor_id in BuoyScraper.VARIABLES.items():
            url = f"{BuoyScraper.BASE_URL}?station_code={BuoyScraper.STATION_CODE}&var_code={var_code}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                if not response.text.strip():
                    logger.error(f"❌ Respuesta vacía para sensor ID {sensor_id}")
                    continue

                df = pd.read_csv(io.StringIO(response.text))

                if df.shape[1] < 2:
                    logger.error(f"❌ Formato inesperado en los datos del sensor ID {sensor_id}")
                    continue

                df.columns = ["timestamp", "value"]
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                df["value"] = pd.to_numeric(df["value"], errors="coerce")

                # Filtrar valores inválidos
                df = df.dropna()

                tuples = [
                    (row["timestamp"], row["value"], quality_flag, processing_level_id, sensor_id, location_id)
                    for _, row in df.iterrows()
                ]
                results.extend(tuples)

            except requests.RequestException as e:
                logger.error(f"❌ Error al obtener datos del sensor ID {sensor_id}: {e}")
            except Exception as e:
                logger.error(f"❌ Error al procesar los datos del sensor ID {sensor_id}: {e}")

        return results  # Devuelve lista de tuplas [(timestamp, value, quality_flag, processing_level_id, sensor_id, location_id)]
