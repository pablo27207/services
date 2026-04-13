from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from db import get_db_connection, safe_float

ocean_bp = Blueprint("ocean", __name__, url_prefix="/api")

BUOY_SENSORS = {
    3: "Altura de Olas",
    4: "Periodo de Olas",
    5: "Dirección de Olas",
    6: "Velocidad de Corriente",
    7: "Dirección de la Corriente",
    8: "Radiación PAR",
    9: "Batería",
}


@ocean_bp.get("/mareograph")
def get_mareograph_data():
    """
    Nivel del mareógrafo — últimos 30 días
    ---
    tags: [Ocean]
    responses:
      200:
        description: Serie temporal del nivel del mar
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  timestamp: { type: string, format: date-time }
                  level:     { type: number, example: 2.34 }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT timestamp, value FROM oogsj_data.measurement
        WHERE sensor_id = 1 AND timestamp >= NOW() - INTERVAL '30 days'
        ORDER BY timestamp;
    """)
    data = [{"timestamp": row[0], "level": safe_float(row[1])} for row in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(data)


@ocean_bp.get("/mareograph/latest")
def get_latest_mareograph_data():
    """
    Último dato del mareógrafo
    ---
    tags: [Ocean]
    responses:
      200:
        description: Último valor registrado por sensor del mareógrafo
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: object
                properties:
                  timestamp: { type: string, format: date-time }
                  value:     { type: number }
                  unit:      { type: string }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT DISTINCT ON (m.sensor_id) s.name, m.timestamp, m.value, u.symbol
        FROM oogsj_data.measurement m
        JOIN oogsj_data.sensor s ON m.sensor_id = s.id
        JOIN oogsj_data.unit   u ON s.unit_id   = u.id
        WHERE s.platform_id = 1
        ORDER BY m.sensor_id, m.timestamp DESC;
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    data = {}
    for name, timestamp, value, unit in rows:
        data[name] = {"timestamp": timestamp,
                      "value": safe_float(value) if value is not None else None,
                      "unit": unit}
    return jsonify(data)


@ocean_bp.get("/buoy")
def get_buoy_data():
    """
    Datos de la boya — últimos 10 días
    ---
    tags: [Ocean]
    responses:
      200:
        description: Series temporales por variable de la boya oceanográfica
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
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
    cur.execute("""
        SELECT sensor_id, timestamp, value FROM oogsj_data.measurement
        WHERE sensor_id IN (3,4,5,6,7,8,9) AND timestamp >= %s
        ORDER BY timestamp;
    """, (desde,))
    raw  = cur.fetchall()
    cur.close(); conn.close()
    data = {name: [] for name in BUOY_SENSORS.values()}
    for sensor_id, timestamp, value in raw:
        name = BUOY_SENSORS.get(sensor_id, f"Sensor {sensor_id}")
        data[name].append({"timestamp": timestamp, "value": value})
    return jsonify(data)


@ocean_bp.get("/buoy/latest")
def get_latest_buoy_data():
    """
    Último dato de la boya por sensor
    ---
    tags: [Ocean]
    responses:
      200:
        description: Último valor registrado por cada sensor de la boya
        content:
          application/json:
            schema:
              type: object
              additionalProperties:
                type: object
                properties:
                  timestamp: { type: string, format: date-time }
                  value:     { type: number }
                  unit:      { type: string }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT DISTINCT ON (m.sensor_id) s.name, m.timestamp, m.value, u.symbol
        FROM oogsj_data.measurement m
        JOIN oogsj_data.sensor s ON m.sensor_id = s.id
        JOIN oogsj_data.unit   u ON s.unit_id   = u.id
        WHERE s.platform_id = 3
        ORDER BY m.sensor_id, m.timestamp DESC;
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    data = {}
    for name, timestamp, value, unit in rows:
        data[name] = {"timestamp": timestamp,
                      "value": safe_float(value) if value is not None else None,
                      "unit": unit}
    return jsonify(data)


@ocean_bp.get("/tide_forecast")
def get_tide_forecast_data():
    """
    Predicción de marea — últimos 10 días
    ---
    tags: [Ocean]
    responses:
      200:
        description: Serie temporal de predicción de marea
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  timestamp: { type: string, format: date-time }
                  level:     { type: number, example: 1.85 }
    """
    conn  = get_db_connection()
    cur   = conn.cursor()
    desde = datetime.utcnow() - timedelta(days=10)
    cur.execute("""
        SELECT timestamp, value FROM oogsj_data.measurement
        WHERE sensor_id = 2 AND timestamp >= %s ORDER BY timestamp;
    """, (desde,))
    data = [{"timestamp": row[0], "level": safe_float(row[1])} for row in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(data)


@ocean_bp.get("/mediciones_negativas")
def mediciones_negativas():
    """
    Mediciones negativas (debug)
    ---
    tags: [Ocean]
    responses:
      200:
        description: Lista de mediciones con valor negativo para control de calidad
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  sensor:    { type: string }
                  valor:     { type: number }
                  timestamp: { type: string, format: date-time }
                  unidad:    { type: string }
    """
    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT s.name, m.value, m.timestamp, u.symbol
        FROM oogsj_data.measurement m
        JOIN oogsj_data.sensor s ON m.sensor_id = s.id
        JOIN oogsj_data.unit   u ON s.unit_id   = u.id
        WHERE m.value < 0 ORDER BY m.timestamp DESC;
    """)
    datos = [{"sensor": r[0], "valor": r[1],
              "timestamp": r[2].isoformat(), "unidad": r[3]}
             for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(datos)