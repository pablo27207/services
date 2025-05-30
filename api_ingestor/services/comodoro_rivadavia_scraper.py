import requests
import psycopg2
import time
from datetime import datetime
import os

API_KEY = os.getenv("API_KEY_PUERTO")
API_SECRET = os.getenv("API_SECRET_PUERTO")
STATION_ID = '160710'
PLATFORM_NAME = 'APPCR Puerto CR'
LOCATION_ID = 1

DB_CONFIG = {
    'dbname': os.getenv("POSTGRES_DB"),
    'user': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD"),
    'host': 'db',
    'port': 5432
}


class WeatherCRScraper:
    @staticmethod
    def convertir_a_si(nombre, valor):
        if nombre == "Temperatura Exterior":
            return (valor - 32) * 5 / 9
        elif nombre == "Presión Barométrica":
            return valor * 33.8639
        elif nombre == "Velocidad del Viento":
            return valor * 0.44704
        return valor

    @staticmethod
    def asegurar_sensor_y_variable(conn, variable_name, unit_name, unit_symbol, sensor_name, platform_id):
        cur = conn.cursor()

        cur.execute("SELECT id FROM oogsj_data.variable WHERE name = %s", (variable_name,))
        var = cur.fetchone()
        if not var:
            cur.execute("INSERT INTO oogsj_data.variable (name) VALUES (%s) RETURNING id", (variable_name,))
            variable_id = cur.fetchone()[0]
        else:
            variable_id = var[0]

        cur.execute("SELECT id FROM oogsj_data.unit WHERE symbol = %s", (unit_symbol,))
        unit = cur.fetchone()
        if not unit:
            cur.execute("INSERT INTO oogsj_data.unit (name, symbol) VALUES (%s, %s) RETURNING id",
                        (unit_name, unit_symbol))
            unit_id = cur.fetchone()[0]
        else:
            unit_id = unit[0]

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

        conn.commit()
        return sensor_id

    @staticmethod
    def fetch_data():
        timestamp = int(time.time())
        url = f"https://api.weatherlink.com/v2/current/{STATION_ID}?t={timestamp}&api-key={API_KEY}"
        headers = {
            "x-api-secret": API_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["sensors"][0]["data"][0]
        else:
            print("❌ Error al consultar la API:", response.status_code)
            return None

    @staticmethod
    def fetch_station_data():
        data = WeatherCRScraper.fetch_data()
        if not data:
            return

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("SELECT id FROM oogsj_data.platform WHERE name = %s", (PLATFORM_NAME,))
        platform = cur.fetchone()
        if not platform:
            print(f"❌ Plataforma '{PLATFORM_NAME}' no encontrada.")
            return
        platform_id = platform[0]

        timestamp = datetime.fromtimestamp(data["ts"])

        variables = {
            "Temperatura Exterior": ("temp_out", "Grados Celsius", "°C"),
            "Humedad Exterior": ("hum_out", "Porcentaje", "%"),
            "Presión Barométrica": ("bar", "Hectopascales", "hPa"),
            "Velocidad del Viento": ("wind_speed", "Metros por segundo", "m/s")
        }

        for nombre, (clave_json, unidad_si, simbolo_si) in variables.items():
            if clave_json in data and data[clave_json] is not None:
                valor_si = WeatherCRScraper.convertir_a_si(nombre, data[clave_json])
                sensor_name = f"Sensor Virtual - {clave_json} - {STATION_ID}"

                sensor_id = WeatherCRScraper.asegurar_sensor_y_variable(
                    conn, nombre, unidad_si, simbolo_si, sensor_name, platform_id
                )

                try:
                    cur.execute("""
                        INSERT INTO oogsj_data.measurement (
                            sensor_id, timestamp, value, quality_flag, processing_level_id, location_id
                        ) VALUES (
                            %s, %s, %s,
                            (SELECT flag FROM oogsj_data.quality_flag WHERE flag = 0),
                            (SELECT id FROM oogsj_data.processing_level WHERE level = 'Raw'),
                            %s
                        )
                        ON CONFLICT (sensor_id, timestamp) DO NOTHING;
                    """, (sensor_id, timestamp, valor_si, LOCATION_ID))
                    print(f"✅ Insertado: {nombre} = {valor_si:.2f}")
                except Exception as e:
                    print(f"❌ Error insertando {nombre}: {e}")
                    conn.rollback()

        conn.commit()
        cur.close()
        conn.close()
