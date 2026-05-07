#!/usr/bin/env python3
"""
backfill_historico_weatherlink.py
==================================
Script ONE-SHOT: descarga TODO el histórico disponible de WeatherLink
e inserta en oogsj_data.measurement usando ON CONFLICT DO NOTHING.

Solo afecta las plataformas meteorológicas:
  - APPCR Puerto CR  (station 160710)
  - APPCR Muelle CC  (station 191512)

Ejecutar UNA sola vez dentro del contenedor api_ingestor:
    python backfill_historico_weatherlink.py

Requisitos en .env:
    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
    API_KEY_PUERTO, API_SECRET_PUERTO
    API_KEY_MUELLE, API_SECRET_MUELLE
"""

import os
import time
import logging
from datetime import datetime, timedelta, timezone

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Configuración ──────────────────────────────────────────────────────────────
DB_CONFIG = {
    "dbname":   os.getenv("POSTGRES_DB"),
    "user":     os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host":     os.getenv("POSTGRES_HOST", "db"),
    "port":     int(os.getenv("POSTGRES_PORT", 5432)),
}

MAX_DAYS_BACK      = 1095   # 3 años hacia atrás
MAX_DIAS_VACIOS    = 30     # se detiene si hay 30 días consecutivos sin datos
DELAY_ENTRE_CALLS  = 2.0    # segundos entre llamadas a la API (rate limit)

# Centinelas WeatherLink (representan "sin dato")
SENTINEL = {-1, 255, 32767, -32768, 32768}

def _es_valido(v):
    return v is not None and v not in SENTINEL and isinstance(v, (int, float))

# ── Conversiones imperial → SI ─────────────────────────────────────────────────
def _f2c(v):     return round((v - 32) * 5.0 / 9.0, 4)
def _mph2ms(v):  return round(v * 0.44704, 4)
def _inhg2hpa(v):return round(v * 33.8639, 4)
def _mi2mi(v):   return round(float(v), 4)   # wind_run se guarda en millas (mi)
def _noop(v):    return round(float(v), 4)


# ── Configuración de estaciones ────────────────────────────────────────────────
#
# Para APPCR Puerto CR el scraper activo crea sensores con prefijo
# "Sensor Virtual - {campo} - {station_id}", usando variables en español.
# El backfill sigue la MISMA convención para que los datos caigan en los
# mismos sensores que ya tienen mediciones recientes.
#
# Para APPCR Muelle CC el scraper activo busca sensores por nombre exacto
# "{campo} - {station_id}" (preconfigurados en init.sql).
# El backfill también sigue esa convención.
#
# Formato de cada campo:
#   "campo_weatherlink": (
#       variable_name,      # nombre en oogsj_data.variable
#       unit_name,          # nombre en oogsj_data.unit (para crear si no existe)
#       unit_symbol,        # símbolo en oogsj_data.unit
#       conversion_fn,      # función que convierte el valor crudo de la API a SI
#       sensor_name,        # nombre en oogsj_data.sensor
#   )

STATION_CONFIGS = [
    {
        "name":        "APPCR Puerto CR",
        "station_id":  "160710",
        "api_key":     os.getenv("API_KEY_PUERTO"),
        "api_secret":  os.getenv("API_SECRET_PUERTO"),
        "location_id": 3,
        "proc_level":  1,   # Raw
        "quality_flag": 0,
        "fields": {
            "temp_out":            ("Temperatura Exterior",   "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - temp_out - 160710"),
            "temp_out_hi":         ("Temp Out Hi",            "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - temp_out_hi - 160710"),
            "temp_out_lo":         ("Temp Out Lo",            "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - temp_out_lo - 160710"),
            "temp_in":             ("Temp In",                "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - temp_in - 160710"),
            "hum_out":             ("Humedad Exterior",       "Porcentaje",               "%",      _noop,     "Sensor Virtual - hum_out - 160710"),
            "hum_in":              ("Hum In",                 "Porcentaje",               "%",      _noop,     "Sensor Virtual - hum_in - 160710"),
            "bar":                 ("Presión Barométrica",    "Hectopascales",            "hPa",    _inhg2hpa, "Sensor Virtual - bar - 160710"),
            "abs_press":           ("Abs Press",              "Hectopascales",            "hPa",    _inhg2hpa, "Sensor Virtual - abs_press - 160710"),
            "bar_noaa":            ("Bar Noaa",               "Hectopascales",            "hPa",    _inhg2hpa, "Sensor Virtual - bar_noaa - 160710"),
            "bar_alt":             ("Bar Alt",                "Hectopascales",            "hPa",    _inhg2hpa, "Sensor Virtual - bar_alt - 160710"),
            "wind_speed":          ("Velocidad del Viento",   "Metros por segundo",       "m/s",    _mph2ms,   "Sensor Virtual - wind_speed - 160710"),
            "wind_speed_avg":      ("Wind Speed Avg",         "Metros por segundo",       "m/s",    _mph2ms,   "Sensor Virtual - wind_speed_avg - 160710"),
            "wind_speed_hi":       ("Wind Speed Hi",          "Metros por segundo",       "m/s",    _mph2ms,   "Sensor Virtual - wind_speed_hi - 160710"),
            "wind_dir_of_prevail": ("Wind Dir Of Prevail",    "Grados",                   "°",      _noop,     "Sensor Virtual - wind_dir_of_prevail - 160710"),
            "wind_dir_of_hi":      ("Wind Dir Of Hi",         "Grados",                   "°",      _noop,     "Sensor Virtual - wind_dir_of_hi - 160710"),
            "wind_run":            ("Wind Run",               "Millas",                   "mi",     _mi2mi,    "Sensor Virtual - wind_run - 160710"),
            "wind_num_samples":    ("Wind Num Samples",       "Número de muestras",       "muestras",_noop,    "Sensor Virtual - wind_num_samples - 160710"),
            "rainfall_clicks":     ("Rainfall Clicks",        "Número de muestras",       "muestras",_noop,    "Sensor Virtual - rainfall_clicks - 160710"),
            "rainfall_mm":         ("Rainfall Mm",            "Milímetros",               "mm",     _noop,     "Sensor Virtual - rainfall_mm - 160710"),
            "rain_rate_hi_clicks": ("Rain Rate Hi Clicks",    "Número de muestras",       "muestras",_noop,    "Sensor Virtual - rain_rate_hi_clicks - 160710"),
            "rain_rate_hi_mm":     ("Rain Rate Hi Mm",        "Milímetros",               "mm",     _noop,     "Sensor Virtual - rain_rate_hi_mm - 160710"),
            "et":                  ("Et",                     "Milímetros",               "mm",     _noop,     "Sensor Virtual - et - 160710"),
            "dew_point_out":       ("Dew Point Out",          "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - dew_point_out - 160710"),
            "heat_index_out":      ("Heat Index Out",         "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - heat_index_out - 160710"),
            "wind_chill":          ("Wind Chill",             "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - wind_chill - 160710"),
            "thw_index":           ("Thw Index",              "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - thw_index - 160710"),
            "wet_bulb":            ("Wet Bulb",               "Grados Celsius",           "°C",     _f2c,      "Sensor Virtual - wet_bulb - 160710"),
            "deg_days_heat":       ("Deg Days Heat",          "Días grado Fahrenheit",    "°F·d",   _noop,     "Sensor Virtual - deg_days_heat - 160710"),
            "deg_days_cool":       ("Deg Days Cool",          "Días grado Fahrenheit",    "°F·d",   _noop,     "Sensor Virtual - deg_days_cool - 160710"),
        },
    },
    {
        "name":        "APPCR Muelle CC",
        "station_id":  "191512",
        "api_key":     os.getenv("API_KEY_MUELLE"),
        "api_secret":  os.getenv("API_SECRET_MUELLE"),
        "location_id": 4,
        "proc_level":  1,   # Raw
        "quality_flag": 0,
        "fields": {
            "temp_in":             ("Temp In",              "Grados Celsius",           "°C",     _f2c,      "temp_in - 191512"),
            "temp_out":            ("Temp Out",             "Grados Celsius",           "°C",     _f2c,      "temp_out - 191512"),
            "temp_out_hi":         ("Temp Out Hi",          "Grados Celsius",           "°C",     _f2c,      "temp_out_hi - 191512"),
            "temp_out_lo":         ("Temp Out Lo",          "Grados Celsius",           "°C",     _f2c,      "temp_out_lo - 191512"),
            "hum_out":             ("Hum Out",              "Porcentaje",               "%",      _noop,     "hum_out - 191512"),
            "bar":                 ("Bar",                  "Hectopascales",            "hPa",    _inhg2hpa, "bar - 191512"),
            "abs_press":           ("Abs Press",            "Hectopascales",            "hPa",    _inhg2hpa, "abs_press - 191512"),
            "bar_noaa":            ("Bar Noaa",             "Hectopascales",            "hPa",    _inhg2hpa, "bar_noaa - 191512"),
            "bar_alt":             ("Bar Alt",              "Hectopascales",            "hPa",    _inhg2hpa, "bar_alt - 191512"),
            "wind_speed_avg":      ("Wind Speed Avg",       "Metros por segundo",       "m/s",    _mph2ms,   "wind_speed_avg - 191512"),
            "wind_speed_hi":       ("Wind Speed Hi",        "Metros por segundo",       "m/s",    _mph2ms,   "wind_speed_hi - 191512"),
            "wind_dir_of_prevail": ("Wind Dir Of Prevail",  "Grados",                   "°",      _noop,     "wind_dir_of_prevail - 191512"),
            "wind_dir_of_hi":      ("Wind Dir Of Hi",       "Grados",                   "°",      _noop,     "wind_dir_of_hi - 191512"),
            "wind_run":            ("Wind Run",             "Unidad desconocida",       "?",      _mi2mi,    "wind_run - 191512"),
            "wind_num_samples":    ("Wind Num Samples",     "Número de muestras",       "muestras",_noop,    "wind_num_samples - 191512"),
            "rainfall_clicks":     ("Rainfall Clicks",      "Número de muestras",       "muestras",_noop,    "rainfall_clicks - 191512"),
            "rainfall_mm":         ("Rainfall Mm",          "Milímetros",               "mm",     _noop,     "rainfall_mm - 191512"),
            "rain_rate_hi_clicks": ("Rain Rate Hi Clicks",  "Número de muestras",       "muestras",_noop,    "rain_rate_hi_clicks - 191512"),
            "rain_rate_hi_mm":     ("Rain Rate Hi Mm",      "Milímetros",               "mm",     _noop,     "rain_rate_hi_mm - 191512"),
            "et":                  ("Et",                   "Milímetros",               "mm",     _noop,     "et - 191512"),
            "dew_point_out":       ("Dew Point Out",        "Grados Celsius",           "°C",     _f2c,      "dew_point_out - 191512"),
            "heat_index_out":      ("Heat Index Out",       "Grados Celsius",           "°C",     _f2c,      "heat_index_out - 191512"),
            "wind_chill":          ("Wind Chill",           "Grados Celsius",           "°C",     _f2c,      "wind_chill - 191512"),
            "thw_index":           ("Thw Index",            "Grados Celsius",           "°C",     _f2c,      "thw_index - 191512"),
            "thsw_index":          ("Thsw Index",           "Grados Celsius",           "°C",     _f2c,      "thsw_index - 191512"),
            "wet_bulb":            ("Wet Bulb",             "Grados Celsius",           "°C",     _f2c,      "wet_bulb - 191512"),
            "solar_rad_avg":       ("Solar Rad Avg",        "Vatios por metro cuadrado","W/m²",   _noop,     "solar_rad_avg - 191512"),
            "solar_rad_hi":        ("Solar Rad Hi",         "Vatios por metro cuadrado","W/m²",   _noop,     "solar_rad_hi - 191512"),
            "solar_energy":        ("Solar Energy",         "Energía solar acumulada",  "Wh/m²",  _noop,     "solar_energy - 191512"),
            "uv_index_avg":        ("Uv Index Avg",         "Índice UV",                "índice", _noop,     "uv_index_avg - 191512"),
            "uv_index_hi":         ("Uv Index Hi",          "Índice UV",                "índice", _noop,     "uv_index_hi - 191512"),
            "uv_dose":             ("Uv Dose",              "Dosis UV acumulada",       "mJ/cm²", _noop,     "uv_dose - 191512"),
            "night_cloud_cover":   ("Night Cloud Cover",    "Número de muestras",       "muestras",_noop,    "night_cloud_cover - 191512"),
            "deg_days_heat":       ("Deg Days Heat",        "Días grado Fahrenheit",    "°F·d",   _noop,     "deg_days_heat - 191512"),
            "deg_days_cool":       ("Deg Days Cool",        "Días grado Fahrenheit",    "°F·d",   _noop,     "deg_days_cool - 191512"),
        },
    },
]

# ── SQL ────────────────────────────────────────────────────────────────────────
INSERT_SQL = """
    INSERT INTO oogsj_data.measurement
        (sensor_id, timestamp, value, quality_flag, processing_level_id, location_id)
    VALUES (%s, to_timestamp(%s), %s, %s, %s, %s)
    ON CONFLICT (sensor_id, timestamp) DO NOTHING;
"""


# ── Helpers BD ─────────────────────────────────────────────────────────────────
def _get_or_create_variable(cur, variable_name):
    cur.execute("SELECT id FROM oogsj_data.variable WHERE name = %s", (variable_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO oogsj_data.variable (name) VALUES (%s) RETURNING id", (variable_name,))
    return cur.fetchone()[0]


def _get_or_create_unit(cur, unit_name, unit_symbol):
    cur.execute("SELECT id FROM oogsj_data.unit WHERE symbol = %s", (unit_symbol,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO oogsj_data.unit (name, symbol) VALUES (%s, %s) RETURNING id",
        (unit_name, unit_symbol),
    )
    return cur.fetchone()[0]


def _get_or_create_sensor(cur, sensor_name, platform_id, variable_id, unit_id):
    cur.execute("SELECT id FROM oogsj_data.sensor WHERE name = %s", (sensor_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO oogsj_data.sensor (platform_id, name, variable_id, unit_id) "
        "VALUES (%s, %s, %s, %s) RETURNING id",
        (platform_id, sensor_name, variable_id, unit_id),
    )
    return cur.fetchone()[0]


def resolver_sensor_ids(conn, station_cfg):
    """
    Devuelve un dict: campo_weatherlink → sensor_id en la BD.
    Crea variable/unidad/sensor si no existen (usando ON CONFLICT implícito
    con las funciones de búsqueda-creación).
    """
    platform_id = _get_platform_id(conn, station_cfg["name"])
    if platform_id is None:
        log.error(f"Plataforma '{station_cfg['name']}' no encontrada en la BD.")
        return {}

    mapping = {}
    with conn.cursor() as cur:
        for campo, (var_name, unit_name, unit_sym, _, sensor_name) in station_cfg["fields"].items():
            try:
                var_id    = _get_or_create_variable(cur, var_name)
                unit_id   = _get_or_create_unit(cur, unit_name, unit_sym)
                sensor_id = _get_or_create_sensor(cur, sensor_name, platform_id, var_id, unit_id)
                mapping[campo] = sensor_id
            except Exception as e:
                log.warning(f"  ⚠️  No se pudo resolver sensor para '{campo}': {e}")
                conn.rollback()
                continue
        conn.commit()

    log.info(f"  ✔ {len(mapping)}/{len(station_cfg['fields'])} sensores resueltos en BD")
    return mapping


def _get_platform_id(conn, platform_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM oogsj_data.platform WHERE name = %s", (platform_name,))
        row = cur.fetchone()
    return row[0] if row else None


# ── API WeatherLink ────────────────────────────────────────────────────────────
def fetch_dia(station_id, api_key, api_secret, day_start: datetime, reintentos=3):
    """Trae todos los registros del endpoint histórico para un día dado."""
    start_ts = int(day_start.timestamp())
    end_ts   = int((day_start + timedelta(days=1)).timestamp())
    url = (
        f"https://api.weatherlink.com/v2/historic/{station_id}"
        f"?t={int(time.time())}&api-key={api_key}"
        f"&start-timestamp={start_ts}&end-timestamp={end_ts}"
    )
    headers = {"x-api-secret": api_secret, "Accept": "application/json"}

    for intento in range(1, reintentos + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
        except requests.RequestException as e:
            log.warning(f"    ⚠️  Error de red (intento {intento}): {e}")
            time.sleep(5 * intento)
            continue

        if resp.status_code == 429:
            wait = 60 * intento
            log.warning(f"    ⏳ Rate limit (429) — esperando {wait}s")
            time.sleep(wait)
            continue

        if resp.status_code != 200:
            log.warning(f"    ⚠️  HTTP {resp.status_code}: {resp.text[:150]}")
            return []

        try:
            js = resp.json()
        except Exception:
            return []

        registros = []
        for sensor in js.get("sensors", []):
            for rec in (sensor.get("data") or []):
                if rec:
                    registros.append(rec)
        return registros

    return []


# ── Inserción ──────────────────────────────────────────────────────────────────
def insertar_registros(conn, registros, sensor_id_map, station_cfg):
    loc = station_cfg["location_id"]
    pl  = station_cfg["proc_level"]
    qf  = station_cfg["quality_flag"]
    insertados = ignorados = 0

    with conn.cursor() as cur:
        for rec in registros:
            ts = rec.get("ts") or rec.get("generated_at")
            if ts is None:
                continue

            for campo, (_, _, _, conv_fn, _) in station_cfg["fields"].items():
                sensor_id = sensor_id_map.get(campo)
                if sensor_id is None:
                    continue

                raw = rec.get(campo)
                if not _es_valido(raw):
                    continue

                try:
                    valor = conv_fn(float(raw))
                except (TypeError, ValueError):
                    continue

                cur.execute(INSERT_SQL, (sensor_id, ts, valor, qf, pl, loc))
                if cur.rowcount:
                    insertados += 1
                else:
                    ignorados += 1

    conn.commit()
    return insertados, ignorados


# ── Lógica principal por estación ──────────────────────────────────────────────
def backfill_estacion(station_cfg):
    name       = station_cfg["name"]
    station_id = station_cfg["station_id"]
    api_key    = station_cfg["api_key"]
    api_secret = station_cfg["api_secret"]

    log.info(f"\n{'='*65}")
    log.info(f"📡  {name}  (station {station_id})")
    log.info(f"{'='*65}")

    if not api_key or not api_secret:
        log.error("  ❌ Credenciales API ausentes. Verificar variables de entorno.")
        return

    conn = psycopg2.connect(**DB_CONFIG)
    try:
        log.info("  🔗 Resolviendo sensores en la BD...")
        sensor_id_map = resolver_sensor_ids(conn, station_cfg)
        if not sensor_id_map:
            return

        # Iterar día a día desde MAX_DAYS_BACK hasta ayer
        now       = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        start_day = now - timedelta(days=MAX_DAYS_BACK)
        yesterday = now - timedelta(days=1)

        total_ins  = total_ign = 0
        dias_vacios = 0
        dia_inicio_real = None

        dia = start_day
        while dia <= yesterday:
            time.sleep(DELAY_ENTRE_CALLS)
            registros = fetch_dia(station_id, api_key, api_secret, dia)

            if not registros:
                dias_vacios += 1
                if dia_inicio_real is None and dias_vacios % 10 == 0:
                    log.info(f"  ⏩ {dia.strftime('%Y-%m-%d')} — buscando inicio de datos...")
                if dias_vacios >= MAX_DIAS_VACIOS and dia_inicio_real is None:
                    log.info(f"  ⏭  {MAX_DIAS_VACIOS} días vacíos consecutivos — avanzando")
                    dias_vacios = 0
            else:
                if dia_inicio_real is None:
                    dia_inicio_real = dia
                    log.info(f"  📌 Primer día con datos: {dia.strftime('%Y-%m-%d')}")
                dias_vacios = 0
                ins, ign = insertar_registros(conn, registros, sensor_id_map, station_cfg)
                total_ins += ins
                total_ign += ign
                log.info(
                    f"  📅 {dia.strftime('%Y-%m-%d')} — "
                    f"{len(registros):4d} registros API | "
                    f"+{ins:5d} insertados | {ign:5d} ya existían"
                )

            dia += timedelta(days=1)

    finally:
        conn.close()

    log.info(
        f"\n  ✅ {name} completado: "
        f"{total_ins:,} insertados — {total_ign:,} duplicados ignorados"
    )


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    log.info("🚀 Backfill histórico APPCR — iniciando")
    log.info(f"   Rango: últimos {MAX_DAYS_BACK} días ({MAX_DAYS_BACK//365} años aprox.)")
    log.info(f"   Delay entre llamadas API: {DELAY_ENTRE_CALLS}s")

    for cfg in STATION_CONFIGS:
        backfill_estacion(cfg)

    log.info("\n🏁 Backfill completo para todas las estaciones")
