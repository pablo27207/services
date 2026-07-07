from datetime import datetime, timedelta, timezone

from flask import Blueprint, jsonify

from db import get_db_connection

emac_cmd1_bp = Blueprint("emac_cmd1", __name__, url_prefix="/api/emac_cmd1")

_PLATFORM_NAME = "Estación EMAC - CMD1"
_STATION_CODE  = "emac_cmd1"

_MS_TO_KMH = 3.6


# ── Utilidades ──────────────────────────────────────────────────────────────
def _ts_to_iso(ts):
    if ts is None:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


# Mapeo variable_name (DB) → clave canónica + label + conversión
_VARIABLE_MAP = {
    "Nivel del Agua":        {"key": "water_level",      "label": "Nivel del Agua",         "src": "m",     "dst": "m"},
    "Temperatura del Agua":  {"key": "water_temperature", "label": "Temperatura del Agua",   "src": "°C",    "dst": "°C"},
    "Conductividad del Agua":{"key": "conductivity",      "label": "Conductividad del Agua", "src": "mS/cm", "dst": "mS/cm"},
    "Temperatura Exterior":  {"key": "air_temperature",   "label": "Temperatura del Aire",   "src": "°C",    "dst": "°C"},
    "Velocidad del Viento":  {"key": "wind_speed",        "label": "Velocidad del Viento",   "src": "m/s",   "dst": "km/h"},
    "Dirección del Viento":  {"key": "wind_direction",    "label": "Dirección del Viento",   "src": "°",     "dst": "°"},
}


def _convert(variable_name, raw):
    """Aplica conversión de unidades según _VARIABLE_MAP. Retorna (valor, unidad)."""
    if raw is None:
        return None, None
    try:
        val = float(raw)
    except (TypeError, ValueError):
        return None, None
    cfg = _VARIABLE_MAP.get(variable_name)
    if not cfg:
        return round(val, 2), None
    if cfg["src"] == "m/s" and cfg["dst"] == "km/h":
        return round(val * _MS_TO_KMH, 2), "km/h"
    return round(val, 2), cfg["dst"]


# ── Último dato ─────────────────────────────────────────────────────────────
@emac_cmd1_bp.get("/")
def get_emac_cmd1_data():
    """
    Estación EMAC CMD1 — último dato
    ---
    tags: [EMAC]
    responses:
      200:
        description: Último registro normalizado de cada variable de la estación EMAC CMD1
        content:
          application/json:
            schema:
              type: object
              properties:
                station_code: { type: string, example: emac_cmd1 }
                station_name: { type: string, example: "Estación EMAC - CMD1" }
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
        """, (_PLATFORM_NAME,))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    if not rows:
        return jsonify({"station_code": _STATION_CODE,
                        "station_name": _PLATFORM_NAME,
                        "timestamp": None, "variables": {}}), 200

    variables  = {}
    latest_ts  = None
    for sid, sensor_name, variable_name, db_unit, ts, raw in rows:
        converted, final_unit = _convert(variable_name, raw)
        cfg = _VARIABLE_MAP.get(variable_name)
        key   = cfg["key"]   if cfg else variable_name.lower().replace(" ", "_")
        label = cfg["label"] if cfg else variable_name
        if ts and (latest_ts is None or ts > latest_ts):
            latest_ts = ts
        variables[key] = {
            "label":     label,
            "sensor":    sensor_name,
            "sensor_id": sid,
            "value":     converted,
            "unit":      final_unit or db_unit,
            "timestamp": _ts_to_iso(ts),
        }

    return jsonify({"station_code": _STATION_CODE,
                    "station_name": _PLATFORM_NAME,
                    "timestamp":    _ts_to_iso(latest_ts),
                    "variables":    variables}), 200


# ── Estado de mantenimiento ───────────────────────────────────────────────────
@emac_cmd1_bp.get("/estado")
def get_emac_cmd1_estado():
    """
    Estación EMAC CMD1 — estado de mantenimiento
    ---
    tags: [EMAC]
    responses:
      200:
        description: Estado de mantenimiento de la plataforma
        content:
          application/json:
            schema:
              type: object
              properties:
                en_mantenimiento: { type: boolean }
                mensaje:          { type: string, nullable: true }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT maintenance_mode, maintenance_message
            FROM oogsj_data.platform WHERE name = %s;
        """, (_PLATFORM_NAME,))
        row = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    if row is None:
        return jsonify({"en_mantenimiento": False, "mensaje": None}), 200
    return jsonify({"en_mantenimiento": bool(row[0]), "mensaje": row[1]}), 200


# ── Histórico ───────────────────────────────────────────────────────────────
@emac_cmd1_bp.get("/history")
def get_emac_cmd1_history():
    """
    Estación EMAC CMD1 — histórico 10 días
    ---
    tags: [EMAC]
    responses:
      200:
        description: >
          Serie temporal de los últimos 10 días agrupada por variable.
          La velocidad del viento se devuelve en km/h (almacenada en m/s).
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: object
                properties:
                  unit:
                    type: string
                    example: km/h
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
        """, (_PLATFORM_NAME, desde))
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    data = {}
    for variable_name, db_unit, ts, raw in rows:
        converted, final_unit = _convert(variable_name, raw)
        cfg = _VARIABLE_MAP.get(variable_name)
        key = cfg["key"] if cfg else variable_name.lower().replace(" ", "_")
        if key not in data:
            data[key] = {"unit": final_unit or db_unit, "data": []}
        data[key]["data"].append({
            "timestamp": _ts_to_iso(ts),
            "value":     converted,
        })

    return jsonify(data), 200
