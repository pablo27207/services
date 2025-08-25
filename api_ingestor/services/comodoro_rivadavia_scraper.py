import requests
import psycopg2
import time
from datetime import datetime, timezone
import os
import logging

# Configurar logging
logging.basicConfig(
    filename="wind_data_filter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    # Valores centinela típicos de WeatherLink (equivalen a “sin dato”)
    SENTINEL = {-1, 255, 32767}

    @staticmethod
    def es_nulo(val):
        """True si el valor es None o un centinela."""
        return val is None or (isinstance(val, (int, float)) and val in WeatherCRScraper.SENTINEL)

    @staticmethod
    def convertir_a_si(nombre, valor):
        if WeatherCRScraper.es_nulo(valor):
            return None
        if nombre == "Temperatura Exterior":
            return (valor - 32) * 5 / 9  # °F → °C
        elif nombre == "Presión Barométrica":
            return valor * 33.8639       # inHg → hPa
        elif nombre == "Velocidad del Viento":
            return valor * 0.44704       # mph → m/s
        return valor

    @staticmethod
    def fetch_data():
        timestamp = int(time.time())
        url = f"https://api.weatherlink.com/v2/current/{STATION_ID}?t={timestamp}&api-key={API_KEY}"
        headers = {
            "x-api-secret": API_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, timeout=12)
        except Exception as e:
            print(f"❌ Error de red consultando la API: {e}")
            return None

        if response.status_code != 200:
            print("❌ Error al consultar la API:", response.status_code, response.text)
            return None

        try:
            return response.json()["sensors"][0]["data"][0]
        except Exception as e:
            print(f"❌ JSON inesperado: {e} / {response.text}")
            return None

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
    def fetch_station_data():
        data = WeatherCRScraper.fetch_data()
        if not data:
            return

        # === Timestamp simple y “a prueba de futuro” ===
        # Usa generated_at (UTC) si existe; si no, usa ts (UTC).
        ts = data.get("generated_at", data.get("ts", int(time.time())))
        timestamp = datetime.fromtimestamp(ts, tz=timezone.utc)
        now_utc = datetime.now(timezone.utc)
        if timestamp > now_utc:
            timestamp = now_utc  # recorte por seguridad

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM oogsj_data.platform WHERE name = %s", (PLATFORM_NAME,))
            platform = cur.fetchone()
            if not platform:
                print(f"❌ Plataforma '{PLATFORM_NAME}' no encontrada.")
                return
            platform_id = platform[0]

            variables = {
                "Temperatura Exterior": ("temp_out", "Grados Celsius", "°C"),
                "Humedad Exterior": ("hum_out", "Porcentaje", "%"),
                "Presión Barométrica": ("bar", "Hectopascales", "hPa"),
                "Velocidad del Viento": ("wind_speed", "Metros por segundo", "m/s")
            }

            for nombre, (clave_json, unidad_si, simbolo_si) in variables.items():
                # Saltear None/centinelas ANTES de convertir
                if clave_json not in data:
                    continue
                valor_crudo = data[clave_json]
                if WeatherCRScraper.es_nulo(valor_crudo):
                    continue

                valor_si = WeatherCRScraper.convertir_a_si(nombre, valor_crudo)
                if valor_si is None:
                    continue

                # Validación mínima: viento no negativo
                if nombre == "Velocidad del Viento" and valor_si < 0:
                    msg = f"Valor negativo descartado para {nombre}: {valor_si:.2f} m/s (ts: {timestamp})"
                    print(f"⚠️ {msg}")
                    logging.info(msg)
                    continue

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
                    """, (sensor_id, timestamp, float(valor_si), LOCATION_ID))
                    print(f"✅ Insertado: {nombre} = {valor_si:.2f} {simbolo_si} @ {timestamp}")
                except Exception as e:
                    print(f"❌ Error insertando {nombre}: {e}")
                    conn.rollback()

            conn.commit()
        finally:
            try:
                cur.close()
            except Exception:
                pass
            conn.close()
