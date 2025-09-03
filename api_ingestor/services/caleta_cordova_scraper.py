# services/caleta_cordova_scraper.py
import os
import psycopg2
from datetime import datetime, timezone
import logging
import time
import requests
#esteee es el malooo deberia borralo pero no se usa, es un ejemplo de como no hacer un scraper
# --- Logging básico (archivo y consola) ---
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def _es_nulo(val, SENTINEL):
    return val is None or (isinstance(val, (int, float)) and val in SENTINEL)

def _f_temp_f_to_c(v, SENTINEL):
    return None if _es_nulo(v, SENTINEL) else (v - 32) * 5.0 / 9.0

def _f_mph_to_ms(v, SENTINEL):
    return None if _es_nulo(v, SENTINEL) else v * 0.44704

def _f_inhg_to_hpa(v, SENTINEL):
    return None if _es_nulo(v, SENTINEL) else v * 33.8639

def insert_minimo_weatherlink(
    API_KEY, API_SECRET, STATION_ID,
    PLATFORM_NAME, DB_CONFIG,
    SENTINEL={-1, 255, 32767},
    LOCATION_ID=4, PROCESSING_LEVEL_ID=1, QUALITY_FLAG=0,
    SENSOR_NAME_MAP=None   # opcional: e.g. {"wind_speed": "wind_speed_avg"}
):
    """
    Inserta 4 variables mínimas (hum_out, bar, wind_speed, temp_out) convertidas a SI.
    Usa ON CONFLICT para evitar duplicados y chequeo anti-stale por sensor.
    """
    SENSOR_NAME_MAP = SENSOR_NAME_MAP or {}

    # 1) Traer payload unificado (solo el más reciente)
    ts_now = int(time.time())
    url = f"https://api.weatherlink.com/v2/current/{STATION_ID}?t={ts_now}&api-key={API_KEY}"
    headers = {"x-api-secret": API_SECRET, "Accept": "application/json"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        logging.warning(f"[WL] Error de red: {e}")
        return

    if resp.status_code != 200:
        logging.warning(f"[WL] HTTP {resp.status_code}: {resp.text[:200]}")
        return

    try:
        js = resp.json()
    except Exception as e:
        logging.warning(f"[WL] JSON inválido: {e}")
        return

    sensors = js.get("sensors") or []
    best, best_ts = {}, None

    for s in sensors:
        for d in (s.get("data") or []):
            ts = d.get("generated_at", d.get("ts"))
            if ts is None:
                continue
            if best_ts is None or ts > best_ts:
                best_ts = ts
                best = dict(d)
            else:
                for k, v in d.items():
                    if k not in best and not _es_nulo(v, SENTINEL):
                        best[k] = v

    if not best or best_ts is None:
        logging.warning("[WL] Respuesta sin datos utilizables.")
        return

    timestamp = datetime.fromtimestamp(best_ts, tz=timezone.utc)
    now_utc = datetime.now(timezone.utc)
    if timestamp > now_utc:
        timestamp = now_utc

    # 2) Conexión
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        # 3) ID plataforma
        cur.execute("SELECT id FROM oogsj_data.platform WHERE name = %s", (PLATFORM_NAME,))
        r = cur.fetchone()
        if not r:
            logging.error(f"❌ Plataforma '{PLATFORM_NAME}' no encontrada.")
            return
        platform_id = r[0]

        # 4) Variables mínimas (las 4 más simples)
        mapping = {
            "hum_out":    (None if _es_nulo(best.get("hum_out"), SENTINEL) else float(best.get("hum_out")), "Porcentaje", "%", "hum_out"),
            "bar":        (_f_inhg_to_hpa(best.get("bar"), SENTINEL), "Hectopascales", "hPa", "bar"),
            "wind_speed": (_f_mph_to_ms(best.get("wind_speed"), SENTINEL), "Metros por segundo", "m/s", "wind_speed"),
            "temp_out":   (_f_temp_f_to_c(best.get("temp_out"), SENTINEL), "Grados Celsius", "°C", "temp_out"),
        }

        for base_key, (valor_si, _unidad, simbolo, sensor_base) in mapping.items():
            if valor_si is None:
                continue

            # Aplicar mapeo (opcional)
            sensor_base = SENSOR_NAME_MAP.get(base_key, sensor_base)
            sensor_name = f"{sensor_base} - {STATION_ID}"

            # 5) Buscar sensor físico
            cur.execute("""
                SELECT id FROM oogsj_data.sensor
                WHERE name = %s AND platform_id = %s
            """, (sensor_name, platform_id))
            r = cur.fetchone()
            if not r:
                logging.warning(f"⚠️ Sensor inexistente: {sensor_name} (plataforma {platform_id}). Salta.")
                continue
            sensor_id = r[0]

            # 6) Anti-stale
            cur.execute("""
                SELECT timezone('UTC', MAX(timestamp))
                FROM oogsj_data.measurement
                WHERE sensor_id = %s
            """, (sensor_id,))
            last_ts = cur.fetchone()[0]
            if last_ts is not None and last_ts.tzinfo is None:
                last_ts = last_ts.replace(tzinfo=timezone.utc)

            if last_ts is not None and timestamp <= last_ts:
                logging.info(f"Skip stale: {sensor_name} @ {timestamp.isoformat()} (last={last_ts.isoformat()})")
                continue

            # 7) Insert
            cur.execute("""
                INSERT INTO oogsj_data.measurement
                (sensor_id, timestamp, value, quality_flag, processing_level_id, location_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (sensor_id, timestamp) DO NOTHING;
            """, (sensor_id, timestamp, float(valor_si), QUALITY_FLAG, PROCESSING_LEVEL_ID, LOCATION_ID))
            logging.info(f"✅ Insert: {sensor_name} = {valor_si:.3f} {simbolo} @ {timestamp.isoformat()}")

        conn.commit()
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


class WeatherCCScraper:
    """
    Wrapper para Celery/CLI. Usa env vars y llama al inserter mínimo.
    """
    # --- API WeatherLink ---
    API_KEY = os.getenv("API_KEY_MUELLE")
    API_SECRET = os.getenv("API_SECRET_MUELLE")
    STATION_ID = "191512"

    # --- Metadatos plataforma/BD ---
    PLATFORM_NAME = "APPCR Muelle CC"
    LOCATION_ID = 4
    PROCESSING_LEVEL_ID = 1
    QUALITY_FLAG = 0

    DB_CONFIG = {
        "dbname": os.getenv("POSTGRES_DB"),
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "host": os.getenv("POSTGRES_HOST") or "db",
        "port": int(os.getenv("POSTGRES_PORT") or 5432),
    }

    SENTINEL = {-1, 255, 32767}

    # Si querés que la velocidad instantánea alimente el sensor "promedio":
    SENSOR_NAME_MAP = {
        "wind_speed": "wind_speed_avg",
    }

    @staticmethod
    def fetch_station_data():
        insert_minimo_weatherlink(
            API_KEY=WeatherCCScraper.API_KEY,
            API_SECRET=WeatherCCScraper.API_SECRET,
            STATION_ID=WeatherCCScraper.STATION_ID,
            PLATFORM_NAME=WeatherCCScraper.PLATFORM_NAME,
            DB_CONFIG=WeatherCCScraper.DB_CONFIG,
            SENTINEL=WeatherCCScraper.SENTINEL,
            LOCATION_ID=WeatherCCScraper.LOCATION_ID,
            PROCESSING_LEVEL_ID=WeatherCCScraper.PROCESSING_LEVEL_ID,
            QUALITY_FLAG=WeatherCCScraper.QUALITY_FLAG,
            SENSOR_NAME_MAP=WeatherCCScraper.SENSOR_NAME_MAP,
        )


# Permite ejecutarlo manualmente dentro del contenedor para test:
if __name__ == "__main__":
    WeatherCCScraper.fetch_station_data()
