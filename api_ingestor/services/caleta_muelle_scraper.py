import requests
import time
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql

# Cargar claves desde archivo .env
load_dotenv(".env")

class WeatherCMScraper:
    """
    Clase para obtener, procesar e insertar datos de la estación meteorológica
    del Muelle de Caleta Córdova en la base de datos.
    """

    # --- Mapeo y Configuración ---
    STATION_ID = "191512"
    PLATFORM_ID = 5
    LOCATION_ID = 4
    PROCESSING_LEVEL_ID = 6  # 6: 'Derived'

    SENSOR_DB_MAP = {
    # 'bar' se mapea a 'bar - 191512' (id 56)
    "bar": {"sensor_id": 56, "unit_name": "hPa", "is_sentinel": False},
    # 'temp_in' se mapea a 'temp_in - 191512' (id 42)
    "temp_in": {"sensor_id": 42, "unit_name": "°C", "is_sentinel": False},
    # 'temp_out' se mapea a 'temp_out - 191512' (id 58)
    "temp_out": {"sensor_id": 58, "unit_name": "°C", "is_sentinel": True},
    # 'wind_speed' se mapea a 'wind_speed_avg - 191512' (id 49)
    "wind_speed": {"sensor_id": 49, "unit_name": "m/s", "is_sentinel": False},
    # 'wind_dir' se mapea a 'wind_dir_of_prevail - 191512' (id 52)
    "wind_dir": {"sensor_id": 52, "unit_name": "grados", "is_sentinel": False},
    # 'dew_point' se mapea a 'dew_point_out - 191512' (id 75)
    "dew_point": {"sensor_id": 75, "unit_name": "°C", "is_sentinel": True},
    # 'heat_index' se mapea a 'heat_index_out - 191512' (id 73)
    "heat_index": {"sensor_id": 73, "unit_name": "°C", "is_sentinel": True},
    # 'wind_chill' se mapea a 'wind_chill - 191512' (id 70)
    "wind_chill": {"sensor_id": 70, "unit_name": "°C", "is_sentinel": True},
    # 'rain_rate_clicks' se mapea a 'rainfall_clicks - 191512' (id 43)
    "rain_rate_clicks": {"sensor_id": 43, "unit_name": "Wh/m²", "is_sentinel": False}
}
    # Crear un diccionario para mapear el sensor/variable a su unidad
    SENSOR_UNITS = {
        "bar": "inHg", "bar_trend": "tendencia", "temp_in": "°F", "hum_in": "%",
        "temp_out": "°F", "hum_out": "%", "wind_speed": "mph", "wind_speed_10_min_avg": "mph",
        "wind_dir": "grados", "rain_rate_clicks": "clicks/min", "rain_rate_in": "in/min",
        "rain_rate_mm": "mm/min", "uv": "índice UV", "solar_rad": "W/m²",
        "rain_storm_clicks": "clicks", "rain_storm_in": "in", "rain_storm_mm": "mm",
        "rain_day_clicks": "clicks", "rain_day_in": "in", "rain_day_mm": "mm",
        "rain_month_clicks": "clicks", "rain_month_in": "in", "rain_month_mm": "mm",
        "rain_year_clicks": "clicks", "rain_year_in": "in", "rain_year_mm": "mm",
        "et_day": "in", "et_month": "in", "et_year": "in", "dew_point": "°F",
        "heat_index": "°F", "wind_chill": "°F", "wind_gust_10_min": "mph"
    }

    @staticmethod
    def obtener_datos_estacion(station_id="191512"):
        """
        Consulta los datos de una estación de WeatherLink, imprime un resumen 
        en consola y retorna un diccionario con los datos y sus unidades.
        """
        API_KEY = os.getenv("API_KEY_MUELLE")
        API_SECRET = os.getenv("API_SECRET_MUELLE")
        timestamp = int(time.time())
        url = f"https://api.weatherlink.com/v2/current/{station_id}?t={timestamp}&api-key={API_KEY}"
        headers = {
            "x-api-secret": API_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        print(f"🌐 Consultando estación {station_id}...")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            json_data = response.json()
            print("✅ Respuesta recibida correctamente.")
            print("=" * 60)
            
            sensor_data_with_units = {}
            for sensor in json_data.get("sensors", []):
                print(f"🔹 Sensor: {sensor.get('name', 'Sin nombre')}")
                for d in sensor.get("data", []):
                    print("  📊 Datos:")
                    for k, v in d.items():
                        unit = WeatherCMScraper.SENSOR_UNITS.get(k, "sin unidad")
                        print(f"    {k}: {v} [{unit}]")
                        sensor_data_with_units[k] = {"value": v, "unit": unit}
                print("-" * 60)
            return sensor_data_with_units
        
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ Error HTTP: {http_err}")
            try:
                print(f"Detalles del error: {response.json()}")
            except:
                pass
            return {}
        except requests.exceptions.RequestException as req_err:
            print(f"❌ Error de conexión: {req_err}")
            return {}

    @staticmethod
    def filtrar_datos_esenciales(datos_crudos):
        """
        Filtra los datos brutos de la API para crear un diccionario más pequeño
        con solo las variables clave.
        """
        if not datos_crudos:
            return {}
        
        claves_esenciales = list(WeatherCMScraper.SENSOR_DB_MAP.keys())
        datos_filtrados = {}
        for key in claves_esenciales:
            if key in datos_crudos:
                datos_filtrados[key] = datos_crudos[key]
        return datos_filtrados

    @staticmethod
    def transformar_unidades_a_metricas(datos):
        """
        Toma un diccionario de datos y convierte las unidades imperiales a métricas.
        """
        datos_transformados = {}
        CONVERSION_FACTORS = {
            "°F": lambda f: (f - 32) * 5/9,
            "mph": lambda mph: mph * 0.44704,
            "inHg": lambda inhg: inhg * 33.8639,
            "clicks/min": lambda clicks: clicks * 10.16
        }

        for key, item in datos.items():
            value = item["value"]
            unit = item["unit"]
            
            if unit in CONVERSION_FACTORS and value is not None:
                if key in WeatherCMScraper.SENSOR_DB_MAP and WeatherCMScraper.SENSOR_DB_MAP[key]["is_sentinel"]:
                    datos_transformados[key] = {"value": value, "unit": unit}
                else:
                    converted_value = CONVERSION_FACTORS[unit](value)
                    new_unit = ""
                    if unit == "°F": new_unit = "°C"
                    elif unit == "mph": new_unit = "m/s"
                    elif unit == "inHg": new_unit = "hPa"
                    elif unit == "clicks/min": new_unit = "mm/h"
                    
                    datos_transformados[key] = {"value": round(converted_value, 2), "unit": new_unit}
            else:
                datos_transformados[key] = item
        return datos_transformados

    @staticmethod
    def asegurar_sensor_y_variable(conn, variable_name, unit_name, unit_symbol, sensor_name, platform_id):
        """
        Verifica si existen la variable, unidad y sensor en la DB.
        Si no existen, los crea dinámicamente y retorna el ID del sensor.
        """
        cur = conn.cursor()

        # 1. Verificar/Crear Variable
        cur.execute("SELECT id FROM oogsj_data.variable WHERE name = %s", (variable_name,))
        var = cur.fetchone()
        if not var:
            cur.execute("INSERT INTO oogsj_data.variable (name) VALUES (%s) RETURNING id", (variable_name,))
            variable_id = cur.fetchone()[0]
        else:
            variable_id = var[0]

        # 2. Verificar/Crear Unidad
        cur.execute("SELECT id FROM oogsj_data.unit WHERE symbol = %s", (unit_symbol,))
        unit = cur.fetchone()
        if not unit:
            cur.execute("INSERT INTO oogsj_data.unit (name, symbol) VALUES (%s, %s) RETURNING id",
                        (unit_name, unit_symbol))
            unit_id = cur.fetchone()[0]
        else:
            unit_id = unit[0]

        # 3. Verificar/Crear Sensor
        cur.execute("SELECT id FROM oogsj_data.sensor WHERE name = %s", (sensor_name,))
        sensor = cur.fetchone()
        if not sensor:
            cur.execute("""
                INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (platform_id, sensor_name, variable_id, unit_id))
            sensor_id = cur.fetchone()[0]
            print(f"✨ Sensor creado: {sensor_name}")
        else:
            sensor_id = sensor[0]

        conn.commit()
        return sensor_id

    @staticmethod
    def insertar_datos_en_bd(datos_esenciales):
        """Inserta los datos procesados en la tabla de mediciones de la base de datos."""
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT")
            )
            cur = conn.cursor()
            
            timestamp = int(time.time())
            
            # Mapeo auxiliar para nombres de variables y unidades (para creación dinámica)
            VAR_INFO = {
                "bar": ("Presión Barométrica", "Hectopascales", "hPa"),
                "temp_in": ("Temperatura Interior", "Grados Celsius", "°C"),
                "temp_out": ("Temperatura Exterior", "Grados Celsius", "°C"),
                "wind_speed": ("Velocidad del Viento", "Metros por segundo", "m/s"),
                "wind_dir": ("Dirección del Viento", "Grados", "°"),
                "dew_point": ("Punto de Rocío", "Grados Celsius", "°C"),
                "heat_index": ("Índice de Calor", "Grados Celsius", "°C"),
                "wind_chill": ("Sensación Térmica", "Grados Celsius", "°C"),
                "rain_rate_clicks": ("Tasa de Lluvia", "Milímetros por hora", "mm/h")
            }

            for key, item in datos_esenciales.items():
                value = item["value"]
                sensor_name_db = f"{key} - {WeatherCMScraper.STATION_ID}"
                
                # 1. Buscar si el sensor ya existe
                cur.execute("SELECT id FROM oogsj_data.sensor WHERE name = %s", (sensor_name_db,))
                result = cur.fetchone()
                
                sensor_id = None
                
                if result:
                    sensor_id = result[0]
                else:
                    # 2. Si no existe, SOLO crearlo si el valor es válido (no None)
                    if value is None:
                        print(f"⚠️ Sensor '{sensor_name_db}' no existe y valor es None. Saltando creación.")
                        continue
                        
                    if key in VAR_INFO:
                        var_name, unit_name, unit_symbol = VAR_INFO[key]
                        sensor_id = WeatherCMScraper.asegurar_sensor_y_variable(
                            conn, var_name, unit_name, unit_symbol, sensor_name_db, WeatherCMScraper.PLATFORM_ID
                        )
                    else:
                        print(f"⚠️ No hay info para crear sensor '{sensor_name_db}'. Saltando...")
                        continue

                # 3. Insertar el dato
                quality_flag = 1  # Bueno
                if value is None:
                    quality_flag = 4 # Malo/Faltante
                
                query = sql.SQL("""
                    INSERT INTO oogsj_data.measurement
                    (sensor_id, timestamp, value, quality_flag, processing_level_id, location_id)
                    VALUES (%s, to_timestamp(%s), %s, %s, %s, %s)
                    ON CONFLICT (sensor_id, timestamp) DO NOTHING;
                """)
                
                cur.execute(query, (
                    sensor_id,
                    timestamp,
                    value,
                    quality_flag,
                    WeatherCMScraper.PROCESSING_LEVEL_ID,
                    WeatherCMScraper.LOCATION_ID
                ))
            
            conn.commit()
            print("✅ Datos insertados en la base de datos correctamente.")

        except psycopg2.Error as e:
            print(f"❌ Error de base de datos: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                cur.close()
                conn.close()

    @staticmethod
    def fetch_station_data():
        """
        Método principal que orquesta la obtención, procesamiento e inserción de datos.
        """
        print(f"--- Ejecutando tarea para la estación {WeatherCMScraper.STATION_ID} ---")
        datos_crudos = WeatherCMScraper.obtener_datos_estacion(WeatherCMScraper.STATION_ID)
        
        if not datos_crudos:
            print("❌ No se obtuvieron datos de la API. Abortando inserción.")
            return

        print("\n✅ Diccionario de datos crudos obtenido.")
        
        datos_filtrados = WeatherCMScraper.filtrar_datos_esenciales(datos_crudos)
        datos_finales = WeatherCMScraper.transformar_unidades_a_metricas(datos_filtrados)
        
        print("\n✅ Diccionario final con unidades métricas y esenciales:")
        print(datos_finales)

        WeatherCMScraper.insertar_datos_en_bd(datos_finales)
        print("--- Tarea finalizada ---")

# Para probar el método directamente (si no usas Celery)
if __name__ == "__main__":
    WeatherCMScraper.fetch_station_data()