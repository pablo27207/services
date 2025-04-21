import requests
import pandas as pd
import io
from datetime import datetime

class BuoyScraper:
    BASE_URL = "http://emac.criba.edu.ar/servicios/getHistoryValues.php"
    STATION_CODE = "EACC"
    
    # Mapeo de códigos de variable a IDs de sensores en la base de datos
    VARIABLES = {
        "14": 3,  # Altura de Olas
        "15": 4,  # Periodo de Olas
        "32": 5,  # Dirección de Olas
        "23": 6,  # Velocidad de Corriente
        "29": 7,  # Dirección de la Corriente
        "33": 8,  # Radiación PAR
        "08": 9   # Batería
    }

    @staticmethod
    def fetch_buoy_data():
        results = []
        quality_flag = 1
        processing_level_id = 1
        location_id = 2

        for var_code, sensor_id in BuoyScraper.VARIABLES.items():
            url = f"{BuoyScraper.BASE_URL}?station_code={BuoyScraper.STATION_CODE}&var_code={var_code}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                if not response.text.strip():
                    raise ValueError("Respuesta vacía")

                df = pd.read_csv(io.StringIO(response.text))

                if df.shape[1] < 2:
                    raise ValueError("Formato inesperado en el CSV")

                df.columns = ["timestamp", "value"]
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
                df["value"] = pd.to_numeric(df["value"], errors="coerce")

                df = df.dropna()

                tuples = [
                    (row["timestamp"], row["value"], quality_flag, processing_level_id, sensor_id, location_id)
                    for _, row in df.iterrows()
                ]
                results.extend(tuples)

            except requests.RequestException as e:
                print(f"[ERROR HTTP] Sensor ID {sensor_id} ({var_code}): {e}")
            except ValueError as e:
                print(f"[ERROR DE DATOS] Sensor ID {sensor_id} ({var_code}): {e}")
            except Exception as e:
                print(f"[ERROR INESPERADO] Sensor ID {sensor_id} ({var_code}): {e}")

        return results
