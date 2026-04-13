from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify

from db import get_db_connection

stations_bp = Blueprint("stations", __name__, url_prefix="/api/appcr")


# ── Utilidades ─────────────────────────────────────────────
def _ts_to_iso(ts):
    if ts is None:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalizar_clave(variable_name, sensor_name):
    texto = f"{(variable_name or '').strip().lower()} {(sensor_name or '').strip().lower()}"
    if "bar" in texto and "bar_trend" not in texto:
        return "barometric_pressure"
    if "dew_point_out" in texto or "dew point out" in texto:
        return "dew_point_outdoor"
    if "heat_index_out" in texto or "heat index out" in texto:
        return "heat_index_outdoor"
    if "temp_in" in texto or "indoor" in texto:
        return "indoor_temperature"
    if "temp_out" in texto or "outdoor temperature" in texto:
        return "outdoor_temperature"
    if "rainfall" in texto or "rain" in texto:
        return "rainfall"
    if "wind_chill" in texto:
        return "wind_chill"
    if "wind_dir_of_prevail" in texto or "wind direction" in texto or "wind_dir" in texto:
        return "wind_direction"
    if "wind_speed_avg" in texto or "wind speed avg" in texto:
        return "wind_speed_avg"
    if "wind_speed" in texto or "wind speed" in texto:
        return "wind_speed"
    if "hum_out" in texto or "humidity out" in texto or "humedad exterior" in texto:
        return "outdoor_humidity"
    clave = (sensor_name or variable_name or "unknown").replace(" ", "_").replace("-", "_").replace("/", "_")
    while "__" in clave:
        clave = clave.replace("__", "_")
    return clave.strip("_")


_LABELS = {
    "barometric_pressure": "Presión barométrica",
    "dew_point_outdoor":   "Punto de rocío exterior",
    "heat_index_outdoor":  "Índice de calor exterior",
    "indoor_temperature":  "Temperatura interior",
    "outdoor_temperature": "Temperatura exterior",
    "rainfall":            "Precipitación",
    "wind_chill":          "Sensación térmica por viento",
    "wind_direction":      "Dirección predominante del viento",
    "wind_speed_avg":      "Velocidad media del viento",
    "wind_speed":          "Velocidad del viento",
    "outdoor_humidity":    "Humedad exterior",
}


def _label(clave, variable_name):
    return _LABELS.get(clave, variable_name if variable_name else clave.replace("_", " ").capitalize())


def _normalizar_unidad_y_valor(clave, unit, val):
    if val is None:
        return unit, None
    try:
        valor = float(val)
    except (TypeError, ValueError):
        return unit, None
    unit_l = (unit or "").strip().lower()
    if clave in ("wind_speed_avg", "wind_speed"):
        if unit_l in ("m/s", "mps", "meter/second", "meters/second"):
            return "km/h", round(valor * 3.6, 2)
        if unit_l in ("km/h", "kmh"):
            return "km/h", round(valor, 2)
    return unit, round(valor, 2)


# ── Muelle CC helpers ──────────────────────────────────────
_VARIABLE_MAP_CC = {
    "Bar":                 {"key": "barometric_pressure", "label": "Presión barométrica",         "src": "hPa",    "dst": "hPa"},
    "Dew Point Out":       {"key": "dew_point_outdoor",   "label": "Punto de rocío exterior",     "src": "°F",     "dst": "°C"},
    "Heat Index Out":      {"key": "heat_index_outdoor",  "label": "Índice de calor exterior",    "src": "°F",     "dst": "°C"},
    "Rainfall Clicks":     {"key": "rainfall",            "label": "Precipitación",               "src": "clicks", "dst": "mm"},
    "Temp In":             {"key": "indoor_temperature",  "label": "Temperatura interior",        "src": "°F",     "dst": "°C"},
    "Temp Out":            {"key": "outdoor_temperature", "label": "Temperatura exterior",        "src": "°F",     "dst": "°C"},
    "Wind Chill":          {"key": "wind_chill",          "label": "Sensación térmica por viento","src": "°F",     "dst": "°C"},
    "Wind Dir Of Prevail": {"key": "wind_direction",      "label": "Dir. predominante del viento","src": "degrees","dst": "degrees"},
    "Wind Speed Avg":      {"key": "wind_speed_avg",      "label": "Velocidad media del viento",  "src": "mph",    "dst": "km/h"},
}


def _convert_cc(variable_name, raw):
    if raw is None:
        return None, None
    cfg = _VARIABLE_MAP_CC.get(variable_name)
    if not cfg:
        return round(raw, 2), None
    src, dst = cfg["src"], cfg["dst"]
    if src == dst:
        return round(raw, 2), "°" if src == "degrees" else dst
    if src == "°F" and dst == "°C":
        return round((raw - 32) * 5 / 9, 2), dst
    if src == "mph" and dst == "km/h":
        return round(raw * 1.60934, 2), dst
    if src == "clicks" and dst == "mm":
        return round(raw * 0.2, 2), dst
    return round(raw, 2), dst


# ── Puerto CR — último dato ────────────────────────────────
@stations_bp.get("/puerto")
def get_puerto_data():
    """
    Estación Puerto CR — último dato
    ---
    tags: [Stations]
    responses:
      200:
        description: Último registro normalizado de cada variable de la estación Puerto CR
        content:
          application/json:
            schema:
              type: object
              properties:
                station_code: { type: string, example: appcr_puerto_cr }
                station_name: { type: string }
                timestamp:    { type: string, format: date-time }
                variables:
                  type: object
                  additionalProperties:
                    type: object
                    properties:
                      label:     { type: string }
                      sensor:    { type: string }
                      sensor_id: { type: integer }
                      value:     { type: number }
                      unit:      { type: string }
                      timestamp: { type: string, format: date-time }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT s.id, s.name, v.name, u.symbol, m."timestamp", m.value
            FROM oogsj_data.platform p
            JOIN oogsj_data.sensor s ON s.platform_id = p.id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit u ON u.id = s.unit_id
            JOIN LATERAL (
                SELECT m2."timestamp", m2.value
                FROM oogsj_data.measurement m2
                WHERE m2.sensor_id = s.id
                ORDER BY m2."timestamp" DESC LIMIT 1
            ) m ON TRUE
            WHERE p.name = %s
            ORDER BY v.name, s.name;
        """, ("APPCR Puerto CR",))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    if not rows:
        return jsonify({"station_code": "appcr_puerto_cr",
                        "station_name": "APPCR Puerto CR",
                        "timestamp": None, "variables": {}}), 200

    variables = {}
    latest_ts = None
    for sid, sensor, variable_name, unit, ts, val in rows:
        clave = _normalizar_clave(variable_name, sensor)
        unit_n, value_n = _normalizar_unidad_y_valor(clave, unit, val)
        variables[clave] = {
            "label": _label(clave, variable_name),
            "sensor": sensor, "sensor_id": sid,
            "timestamp": _ts_to_iso(ts),
            "unit": unit_n, "value": value_n,
        }
        if ts and (latest_ts is None or ts > latest_ts):
            latest_ts = ts

    return jsonify({"station_code": "appcr_puerto_cr",
                    "station_name": "APPCR Puerto CR",
                    "timestamp": _ts_to_iso(latest_ts),
                    "variables": variables}), 200


# ── Puerto CR — histórico ──────────────────────────────────
@stations_bp.get("/puerto/history")
def get_puerto_history():
    """
    Estación Puerto CR — histórico 10 días
    ---
    tags: [Stations]
    responses:
      200:
        description: Serie temporal de los últimos 10 días agrupada por variable
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: object
                properties:
                  unit: { type: string }
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        timestamp: { type: string, format: date-time }
                        value:     { type: number }
    """
    conn  = get_db_connection()
    cur   = conn.cursor()
    desde = datetime.utcnow() - timedelta(days=10)
    try:
        cur.execute("""
            SELECT v.name, u.symbol, m."timestamp", m.value
            FROM oogsj_data.measurement m
            JOIN oogsj_data.sensor   s ON s.id = m.sensor_id
            JOIN oogsj_data.platform p ON p.id = s.platform_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            WHERE p.name = %s AND m."timestamp" >= %s
            ORDER BY v.name, m."timestamp";
        """, ("APPCR Puerto CR", desde))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    data = {}
    for variable_name, unit, ts, val in rows:
        if variable_name not in data:
            data[variable_name] = {"unit": unit, "data": []}
        data[variable_name]["data"].append({
            "timestamp": ts.isoformat() if ts else None,
            "value":     float(val) if val is not None else None,
        })
    return jsonify(data)


# ── Muelle CC — último dato ────────────────────────────────
@stations_bp.get("/muelle_cc")
def get_muelle_cc_data():
    """
    Estación Muelle CC — último dato
    ---
    tags: [Stations]
    responses:
      200:
        description: Último registro normalizado de cada variable de la estación Muelle CC
        content:
          application/json:
            schema:
              type: object
              properties:
                station_code: { type: string, example: appcr_muelle_cc }
                station_name: { type: string }
                timestamp:    { type: string, format: date-time }
                variables:
                  type: object
                  additionalProperties:
                    type: object
                    properties:
                      label:     { type: string }
                      sensor:    { type: string }
                      sensor_id: { type: integer }
                      value:     { type: number }
                      unit:      { type: string }
                      timestamp: { type: string, format: date-time }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT s.id, s.name, v.name, u.symbol, m."timestamp", m.value
            FROM oogsj_data.platform p
            JOIN oogsj_data.sensor   s ON s.platform_id = p.id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN LATERAL (
                SELECT m2."timestamp", m2.value
                FROM oogsj_data.measurement m2
                WHERE m2.sensor_id = s.id
                ORDER BY m2."timestamp" DESC LIMIT 1
            ) m ON TRUE
            WHERE p.name = %s
            ORDER BY v.name, s.name;
        """, ("APPCR Muelle CC",))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    if not rows:
        return jsonify({"station_name": "APPCR Muelle CC",
                        "station_code": "appcr_muelle_cc",
                        "timestamp": None, "variables": {}}), 200

    variables = {}
    latest_ts = None
    for sid, sensor_name, variable_name, db_unit, ts, raw in rows:
        raw_val = float(raw) if raw is not None else None
        cfg = _VARIABLE_MAP_CC.get(variable_name)
        converted, final_unit = _convert_cc(variable_name, raw_val)
        key   = cfg["key"]   if cfg else variable_name.lower().replace(" ", "_")
        label = cfg["label"] if cfg else variable_name
        if ts and (latest_ts is None or ts > latest_ts):
            latest_ts = ts
        variables[key] = {
            "label": label, "sensor": sensor_name, "sensor_id": sid,
            "value": converted, "unit": final_unit or db_unit,
            "timestamp": _ts_to_iso(ts),
        }

    return jsonify({"station_name": "APPCR Muelle CC",
                    "station_code": "appcr_muelle_cc",
                    "timestamp": _ts_to_iso(latest_ts),
                    "variables": variables}), 200


# ── Muelle CC — histórico ──────────────────────────────────
@stations_bp.get("/muelle_cc/history")
def get_muelle_cc_history():
    """
    Estación Muelle CC — histórico 15 días
    ---
    tags: [Stations]
    responses:
      200:
        description: Serie temporal de los últimos 15 días agrupada por variable
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: object
                properties:
                  unit: { type: string }
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        timestamp: { type: string, format: date-time }
                        value:     { type: number }
    """
    conn  = get_db_connection()
    cur   = conn.cursor()
    desde = datetime.utcnow() - timedelta(days=15)
    try:
        cur.execute("""
            SELECT v.name, m.timestamp, m.value, u.symbol
            FROM oogsj_data.measurement m
            JOIN oogsj_data.sensor   s ON s.id = m.sensor_id
            JOIN oogsj_data.variable v ON v.id = s.variable_id
            JOIN oogsj_data.unit     u ON u.id = s.unit_id
            WHERE s.name LIKE '%%160710%%'
              AND m.timestamp >= %s
            ORDER BY v.name, m.timestamp;
        """, (desde,))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    data = {}
    for variable_name, ts, val, unit in rows:
        if variable_name not in data:
            data[variable_name] = {"unit": unit, "data": []}
        data[variable_name]["data"].append({
            "timestamp": ts.isoformat(),
            "value":     float(val),
        })
    return jsonify(data)