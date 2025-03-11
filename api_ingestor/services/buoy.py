import requests
import logging
import pandas as pd
import io

# Configuración del logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BuoyScraper:
    BASE_URL = "http://emac.criba.edu.ar/servicios/getHistoryValues.php"
    STATION_CODE = "EACC"
    VARIABLES = {
        "14": "altura_olas",
        "15": "periodo_olas",
        "32": "direccion_olas",
        "23": "velocidad_corriente",
        "29": "direccion_corriente",
        "33": "radiacion_par",
        "08": "bateria"
    }

    @staticmethod
    def fetch_buoy_data():
        results = []
        for var_code, var_name in BuoyScraper.VARIABLES.items():
            url = f"{BuoyScraper.BASE_URL}?station_code={BuoyScraper.STATION_CODE}&var_code={var_code}"
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # Verificar si la respuesta está vacía
                if not response.text.strip():
                    logger.error(f"❌ Respuesta vacía para {var_name}")
                    continue

                # Procesar CSV con pandas
                df = pd.read_csv(io.StringIO(response.text))

                # Verificar que el CSV tiene al menos dos columnas (Fecha y Valor)
                if df.shape[1] < 2:
                    logger.error(f"❌ Formato inesperado en los datos de {var_name}")
                    continue

                # Renombrar columnas si no tienen encabezado
                df.columns = ["timestamp", var_name]

                # Convertir timestamp a datetime
                df["timestamp"] = pd.to_datetime(df["timestamp"])

                # Convertir valores numéricos
                df[var_name] = pd.to_numeric(df[var_name], errors="coerce")

                # Transformar DataFrame en lista de tuplas [(timestamp, variable, value)]
                tuples = [(row["timestamp"], var_name, row[var_name]) for _, row in df.iterrows()]
                results.extend(tuples)

            except requests.RequestException as e:
                logger.error(f"❌ Error al obtener datos de la boya ({var_name}): {e}")
            except Exception as e:
                logger.error(f"❌ Error al procesar los datos de la boya ({var_name}): {e}")

        return results  # Ahora devuelve una lista de tuplas [(timestamp, variable, value)]
