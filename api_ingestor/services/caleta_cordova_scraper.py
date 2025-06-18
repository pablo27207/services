import requests
import psycopg2
from datetime import datetime
import time
import logging
from .config import get_env_var

# Configurar logging para registrar valores descartados
logging.basicConfig(
    filename="wind_data_filter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class WeatherCCScraper:
    API_KEY = get_env_var("API_KEY_MUELLE")
    API_SECRET = get_env_var("API_SECRET_MUELLE")
    STATION_ID = "191512"
    PLATFORM_NAME = "APPCR Muelle CC"
    LOCATION_ID = 4
    PROCESSING_LEVEL_ID = 1
    QUALITY_FLAG = 0

    DB_CONFIG = {
        'dbname': get_env_var("POSTGRES_DB"),
        'user': get_env_var("POSTGRES_USER"),
        'password': get_env_var("POSTGRES_PASSWORD"),
        'host': 'db',
        'port': 5432
    }

    @staticmethod
    def convertir_a_si(nombre, valor):
        """Convierte valores a unidades del Sistema Internacional (SI)."""
        if nombre in ["Temperatura Exterior", "Temperatura Interior", "Sensación Térmica", "Punto de Rocío", "Índice de Calor"]:
            return (valor - 32) * 5 / 9  # °F → °C
        elif nombre in ["Velocidad del Viento", "Viento Promedio 10 min", "Ráfaga de Viento 10 min"]:
            return valor * 0.44704  # mph → m/s
        elif nombre == "Presión Barométrica":
            return valor * 33.8639  # inHg → hPa
        elif nombre == "Tasa de Lluvia":
            return valor * 25.4  # in → mm
        return valor  # ya en unidades SI

    @staticmethod
    def fetch_data():
        """Consulta la API de WeatherLink y devuelve los datos crudos."""
        timestamp = int(time.time())
        url = f"https://api.weatherlink.com/v2/current/{WeatherCCScraper.STATION_ID}?t={timestamp}&api-key={WeatherCCScraper.API_KEY}"
        headers = {
            "x-api-secret": WeatherCCScraper.API_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["sensors"][0]["data"][0]
        else:
            print("❌ Error al consultar API:", response.status_code)
            return None

    @staticmethod
    def fetch_station_data():
        """Procesa y guarda los datos en la base de datos."""
        data = WeatherCCScraper.fetch_data()
        if not data:
            return

        conn = psycopg2.connect(**WeatherCCScraper.DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT id FROM oogsj_data.platform WHERE name = %s", (WeatherCCScraper.PLATFORM_NAME,))
        platform = cur.fetchone()
        if not platform:
            print(f"❌ Plataforma '{WeatherCCScraper.PLATFORM_NAME}' no encontrada.")
            return
        platform_id = platform[0]

        timestamp = datetime.fromtimestamp(data["ts"])

        variables = {
            "Temperatura Interior": ("temp_in", "Grados Celsius", "°C"),
            "Temperatura Exterior": ("temp_out", "Grados Celsius", "°C"),
            "Punto de Rocío": ("dew_point", "Grados Celsius", "°C"),
            "Índice de Calor": ("heat_index", "Grados Celsius", "°C"),
            "Sensación Térmica": ("wind_chill", "Grados Celsius", "°C"),
            "Velocidad del Viento": ("wind_speed", "Metros por segundo", "m/s"),
            "Viento Promedio 10 min": ("wind_speed_10_min_avg", "Metros por segundo", "m/s"),
            "Ráfaga de Viento 10 min": ("wind_gust_10_min", "Metros por segundo", "m/s"),
            "Dirección del Viento": ("wind_dir", "Grados", "°"),
            "Presión Barométrica": ("bar", "Hectopascales", "hPa"),
            "Humedad Exterior": ("hum_out", "Porcentaje", "%"),
            "Radiación Solar Promedio": ("solar_rad", "W/m²", "W/m²"),
            "ET Diaria": ("et_day", "Milímetros", "mm"),
            "Tasa de Lluvia": ("rain_rate_in", "Milímetros por hora", "mm/h")
        }

        for nombre, (clave_json, unidad_si, simbolo_si) in variables.items():
            if clave_json in data and data[clave_json] is not None:
                valor_si = WeatherCCScraper.convertir_a_si(nombre, data[clave_json])

                # ================= VALIDACIÓN DE RANGO PARA VARIABLES DE VIENTO ===============
                if nombre in ["Velocidad del Viento", "Viento Promedio 10 min", "Ráfaga de Viento 10 min"]:
                    if valor_si < 0 or valor_si > 100:  # ❗ descartamos si es negativo o mayor a 100 m/s
                        msg = f"Valor fuera de rango descartado para {nombre}: {valor_si:.2f} m/s (timestamp: {timestamp})"
                        print(f"⚠️ {msg}")           # Mostramos por consola
                        logging.info(msg)            # Y lo registramos en el archivo log
                        continue                     # ⛔ Saltamos al siguiente dato
                # =============================================================================

                sensor_name = f"Sensor Virtual - {clave_json} - {WeatherCCScraper.STATION_ID}"

                # Asegurar existencia de variable
                cur.execute("SELECT id FROM oogsj_data.variable WHERE name = %s", (nombre,))
                var = cur.fetchone()
                if not var:
                    cur.execute("INSERT INTO oogsj_data.variable (name) VALUES (%s) RETURNING id", (nombre,))
                    variable_id = cur.fetchone()[0]
                else:
                    variable_id = var[0]

                # Asegurar existencia de unidad
                cur.execute("SELECT id FROM oogsj_data.unit WHERE symbol = %s", (simbolo_si,))
                unit = cur.fetchone()
                if not unit:
                    cur.execute("INSERT INTO oogsj_data.unit (name, symbol) VALUES (%s, %s) RETURNING id",
                                (unidad_si, simbolo_si))
                    unit_id = cur.fetchone()[0]
                else:
                    unit_id = unit[0]

                # Asegurar existencia de sensor
                cur.execute("SELECT id FROM oogsj_data.sensor WHERE name = %s", (sensor_name,))
                sensor = cur.fetchone()
                if not sensor:
                    cur.execute("""
                        INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
                        VALUES (%s, %s, %s, %s) RETURNING id
                    """, (platform_id, sensor_name, variable_id, unit_id))
                    sensor_id = cur.fetchone()[0]
                else:
                    sensor_id = sensor[0]

                try:
                    cur.execute("""
                        INSERT INTO oogsj_data.measurement (
                            sensor_id, timestamp, value, quality_flag, processing_level_id, location_id
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s
                        )
                        ON CONFLICT (sensor_id, timestamp) DO NOTHING;
                    """, (
                        sensor_id, timestamp, valor_si,
                        WeatherCCScraper.QUALITY_FLAG,
                        WeatherCCScraper.PROCESSING_LEVEL_ID,
                        WeatherCCScraper.LOCATION_ID
                    ))
                    print(f"✅ Insertado: {nombre} = {valor_si:.2f}")
                except Exception as e:
                    print(f"❌ Error insertando {nombre}: {e}")
                    conn.rollback()


        conn.commit()
        cur.close()
        conn.close()
