import requests
import psycopg2
from datetime import datetime, timezone
import time
import logging
from .config import get_env_var

# === Logging básico ===
logging.basicConfig(
    filename="wind_data_filter.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class WeatherCCScraper:
    # === Config API ===
    API_KEY = get_env_var("API_KEY_MUELLE")
    API_SECRET = get_env_var("API_SECRET_MUELLE")
    STATION_ID = "191512"

    # === Metadatos de plataforma ===
    PLATFORM_NAME = "APPCR Muelle CC"
    LOCATION_ID = 4
    PROCESSING_LEVEL_ID = 1
    QUALITY_FLAG = 0

    # === Config DB ===
    DB_CONFIG = {
        'dbname': get_env_var("POSTGRES_DB"),
        'user': get_env_var("POSTGRES_USER"),
        'password': get_env_var("POSTGRES_PASSWORD"),
        'host': get_env_var("POSTGRES_HOST") or 'db',
        'port': int(get_env_var("POSTGRES_PORT") or 5432),
    }

    # === Centinelas de WeatherLink (sin dato) ===
    SENTINEL = {-1, 255, 32767}

    @staticmethod
    def es_nulo(val):
        """True si el valor es None o un centinela."""
        return val is None or (isinstance(val, (int, float)) and val in WeatherCCScraper.SENTINEL)

    @staticmethod
    def valor_metric(d, k_mm, k_in, factor=25.4):
        """
        Si existe k_mm, devuelve ese valor; si no, convierte k_in (pulgadas→mm por defecto).
        Devuelve None si no hay dato válido.
        """
        v_mm = d.get(k_mm)
        if not WeatherCCScraper.es_nulo(v_mm):
            return v_mm
        v_in = d.get(k_in)
        if not WeatherCCScraper.es_nulo(v_in):
            return v_in * factor
        return None

    @staticmethod
    def convertir_a_si(nombre, valor):
        """Convierte valores a unidades SI (cuando aplica)."""
        if WeatherCCScraper.es_nulo(valor):
            return None
        if nombre in ["Temperatura Exterior", "Temperatura Interior", "Sensación Térmica", "Punto de Rocío", "Índice de Calor"]:
            return (valor - 32) * 5.0 / 9.0  # °F → °C
        if nombre in ["Velocidad del Viento", "Viento Promedio 10 min", "Ráfaga de Viento 10 min"]:
            return valor * 0.44704  # mph → m/s
        if nombre == "Presión Barométrica":
            return valor * 33.8639  # inHg → hPa
        if nombre == "Tasa de Lluvia":
            return valor * 25.4  # in → mm
        return valor  # ya métrico o sin conversión

    @staticmethod
    def fetch_data():
        """Consulta la API de WeatherLink y devuelve el dict 'data' más reciente (primer sensor -> primer data)."""
        ts_now = int(time.time())
        url = f"https://api.weatherlink.com/v2/current/{WeatherCCScraper.STATION_ID}?t={ts_now}&api-key={WeatherCCScraper.API_KEY}"
        headers = {
            "x-api-secret": WeatherCCScraper.API_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"❌ Error al consultar API: {resp.status_code} - {resp.text}")
            return None

        js = resp.json()
        try:
            return js["sensors"][0]["data"][0]
        except Exception as e:
            print(f"❌ JSON inesperado: {e} / {js}")
            return None

    @staticmethod
    def fetch_station_data():
        """Procesa y guarda los datos en la base de datos."""
        data = WeatherCCScraper.fetch_data()
        if not data:
            return

        # === Timestamp simple y seguro ===
        # Usa generated_at (UTC) si existe; si no, usa ts (UTC).
        timestamp = datetime.fromtimestamp(data.get("generated_at", data["ts"]), tz=timezone.utc)
        now_utc = datetime.now(timezone.utc)
        if timestamp > now_utc:
            # Si por cualquier motivo viene en el futuro, ajustamos a "ahora"
            timestamp = now_utc

        # Conexión a DB
        conn = psycopg2.connect(**WeatherCCScraper.DB_CONFIG)
        cur = conn.cursor()
        try:
            # Verificar plataforma
            cur.execute("SELECT id FROM oogsj_data.platform WHERE name = %s", (WeatherCCScraper.PLATFORM_NAME,))
            row = cur.fetchone()
            if not row:
                print(f"❌ Plataforma '{WeatherCCScraper.PLATFORM_NAME}' no encontrada.")
                return
            platform_id = row[0]

            # === Getters con SI y filtros ===
            def f_temp_f_to_c(v):  # °F → °C
                return None if WeatherCCScraper.es_nulo(v) else (v - 32) * 5.0 / 9.0

            def f_mph_to_ms(v):    # mph → m/s
                return None if WeatherCCScraper.es_nulo(v) else v * 0.44704

            def f_inhg_to_hpa(v):  # inHg → hPa
                return None if WeatherCCScraper.es_nulo(v) else v * 33.8639

            def identity(v):       # sin conversión
                return None if WeatherCCScraper.es_nulo(v) else v

            variables = {
                # nombre_visible: (getter, clave/doble_clave, unidad, símbolo)
                "Temperatura Interior": (lambda d: f_temp_f_to_c(d.get("temp_in")), "temp_in", "Grados Celsius", "°C"),
                "Temperatura Exterior": (lambda d: f_temp_f_to_c(d.get("temp_out")), "temp_out", "Grados Celsius", "°C"),
                "Punto de Rocío":       (lambda d: f_temp_f_to_c(d.get("dew_point")), "dew_point", "Grados Celsius", "°C"),
                "Índice de Calor":      (lambda d: f_temp_f_to_c(d.get("heat_index")), "heat_index", "Grados Celsius", "°C"),
                "Sensación Térmica":    (lambda d: f_temp_f_to_c(d.get("wind_chill")), "wind_chill", "Grados Celsius", "°C"),

                "Velocidad del Viento":     (lambda d: f_mph_to_ms(d.get("wind_speed")), "wind_speed", "Metros por segundo", "m/s"),
                "Viento Promedio 10 min":   (lambda d: f_mph_to_ms(d.get("wind_speed_10_min_avg")), "wind_speed_10_min_avg", "Metros por segundo", "m/s"),
                "Ráfaga de Viento 10 min":  (lambda d: f_mph_to_ms(d.get("wind_gust_10_min")), "wind_gust_10_min", "Metros por segundo", "m/s"),

                "Dirección del Viento": (lambda d: identity(d.get("wind_dir")), "wind_dir", "Grados", "°"),
                "Presión Barométrica":  (lambda d: f_inhg_to_hpa(d.get("bar")), "bar", "Hectopascales", "hPa"),
                "Humedad Exterior":     (lambda d: identity(d.get("hum_out")), "hum_out", "Porcentaje", "%"),
                "Radiación Solar Promedio": (lambda d: identity(d.get("solar_rad")), "solar_rad", "W/m²", "W/m²"),

                # Lluvia/ET: si viene en mm, usarlo; si no, convertir pulgadas→mm
                "Tasa de Lluvia": (lambda d: WeatherCCScraper.valor_metric(d, "rain_rate_mm", "rain_rate_in", 25.4),
                                   ("rain_rate_mm", "rain_rate_in"), "Milímetros por hora", "mm/h"),
                "ET Diaria":      (lambda d: None if WeatherCCScraper.es_nulo(d.get("et_day")) else d.get("et_day") * 25.4,
                                   "et_day", "Milímetros", "mm"),
            }

            # === Chequeos suaves de rango (opcional, pero útil) ===
            def dentro_rango(nombre, valor, simbolo):
                if valor is None:
                    return False
                if nombre.startswith("Velocidad") or nombre.startswith("Viento"):
                    if "m/s" in simbolo and not (0 <= valor <= 100):
                        logging.info(f"Descartado {nombre} fuera de rango: {valor:.2f} {simbolo} ({timestamp.isoformat()})")
                        return False
                if nombre.startswith("Temperatura"):
                    if not (-60 <= valor <= 60):
                        logging.info(f"Descartado {nombre} fuera de rango: {valor:.2f} {simbolo} ({timestamp.isoformat()})")
                        return False
                if nombre == "Presión Barométrica" and not (870 <= valor <= 1085):
                    logging.info(f"Descartado {nombre} fuera de rango: {valor:.2f} {simbolo} ({timestamp.isoformat()})")
                    return False
                if nombre == "Humedad Exterior" and not (0 <= valor <= 100):
                    logging.info(f"Descartado {nombre} fuera de rango: {valor:.2f} {simbolo} ({timestamp.isoformat()})")
                    return False
                if nombre == "Dirección del Viento" and not (0 <= valor <= 360):
                    logging.info(f"Descartado {nombre} fuera de rango: {valor:.2f} {simbolo} ({timestamp.isoformat()})")
                    return False
                return True

            # === Loop de variables → insertar ===
            for nombre, (getter, clave_json, unidad_si, simbolo_si) in variables.items():
                valor_si = getter(data)
                if valor_si is None:
                    continue
                if not dentro_rango(nombre, valor_si, simbolo_si):
                    continue

                base_key = clave_json[0] if isinstance(clave_json, tuple) else clave_json
                sensor_name = f"Sensor Virtual - {base_key} - {WeatherCCScraper.STATION_ID}"

                # variable
                cur.execute("SELECT id FROM oogsj_data.variable WHERE name = %s", (nombre,))
                row_var = cur.fetchone()
                if row_var:
                    variable_id = row_var[0]
                else:
                    cur.execute("INSERT INTO oogsj_data.variable (name) VALUES (%s) RETURNING id", (nombre,))
                    variable_id = cur.fetchone()[0]

                # unidad
                cur.execute("SELECT id FROM oogsj_data.unit WHERE symbol = %s", (simbolo_si,))
                row_unit = cur.fetchone()
                if row_unit:
                    unit_id = row_unit[0]
                else:
                    cur.execute(
                        "INSERT INTO oogsj_data.unit (name, symbol) VALUES (%s, %s) RETURNING id",
                        (unidad_si, simbolo_si)
                    )
                    unit_id = cur.fetchone()[0]

                # sensor
                cur.execute("SELECT id FROM oogsj_data.sensor WHERE name = %s", (sensor_name,))
                row_sensor = cur.fetchone()
                if row_sensor:
                    sensor_id = row_sensor[0]
                else:
                    cur.execute(
                        """
                        INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id)
                        VALUES (%s, %s, %s, %s) RETURNING id
                        """,
                        (platform_id, sensor_name, variable_id, unit_id)
                    )
                    sensor_id = cur.fetchone()[0]

                # insert
                try:
                    cur.execute(
                        """
                        INSERT INTO oogsj_data.measurement (
                            sensor_id, timestamp, value, quality_flag, processing_level_id, location_id
                        )
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (sensor_id, timestamp) DO NOTHING;
                        """,
                        (
                            sensor_id,
                            timestamp,  # timestamp seguro (no futuro)
                            float(valor_si),
                            WeatherCCScraper.QUALITY_FLAG,
                            WeatherCCScraper.PROCESSING_LEVEL_ID,
                            WeatherCCScraper.LOCATION_ID,
                        )
                    )
                    print(f"✅ Insertado: {nombre} = {valor_si:.3f} {simbolo_si} @ {timestamp}")
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

if __name__ == "__main__":
    WeatherCCScraper.fetch_station_data()
