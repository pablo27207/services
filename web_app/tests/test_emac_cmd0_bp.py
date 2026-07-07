"""
Tests de web_app/blueprints/emac_cmd0_bp.py — estación EMAC Caleta Córdova.

Cubre:
  - GET /api/emac_cmd0/          (último dato por variable)
  - GET /api/emac_cmd0/history   (histórico 10 días agrupado por variable)

La DB nunca se toca de verdad: se mockea get_db_connection() para que
devuelva un cursor con filas controladas por el test.
"""
from datetime import datetime


def test_get_data_sin_filas_devuelve_estructura_vacia(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchall.return_value = []
    mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd0/")

    assert resp.status_code == 200
    body = resp.get_json()
    assert body == {
        "station_code": "emac_cmd0",
        "station_name": "Estación EMAC - Caleta Córdova CMD0",
        "timestamp": None,
        "variables": {},
    }
    cur.close.assert_called_once()
    conn.close.assert_called_once()


def test_get_data_con_filas_devuelve_variables_normalizadas(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 10, 40, 0)
    cur.fetchall.return_value = [
        # sid, sensor_name, variable_name, db_unit, ts, raw
        (10, "Sensor de Temperatura del Agua - CMD0", "Temperatura del Agua", "°C", ts, "8.13"),
        (11, "Sensor de Velocidad del Viento - CMD0", "Velocidad del Viento", "m/s", ts, "10.0"),
    ]
    mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd0/")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body["station_code"] == "emac_cmd0"
    assert body["timestamp"] == "2026-07-06T10:40:00Z"

    agua = body["variables"]["water_temperature"]
    assert agua["value"] == 8.13
    assert agua["unit"] == "°C"
    assert agua["sensor_id"] == 10

    viento = body["variables"]["wind_speed"]
    # Regresión: el valor se almacena en m/s y la API debe convertirlo a km/h (x3.6).
    assert viento["value"] == 36.0
    assert viento["unit"] == "km/h"


def test_get_data_con_valor_nulo_no_rompe(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 10, 40, 0)
    cur.fetchall.return_value = [
        (10, "Sensor de Nivel del Agua - CMD0", "Nivel del Agua", "m", ts, None),
    ]
    mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd0/")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body["variables"]["water_level"]["value"] is None
    assert body["variables"]["water_level"]["unit"] == "m"  # cae al db_unit


def test_get_data_con_variable_desconocida_usa_fallback(client, db_double, mocker):
    """Si la variable no está en _VARIABLE_MAP, se genera una key/label genéricos."""
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 10, 40, 0)
    cur.fetchall.return_value = [
        (99, "Sensor Nuevo Sin Mapear", "Presion Rara", "hPa", ts, "1013.25"),
    ]
    mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd0/")
    body = resp.get_json()

    var = body["variables"]["presion_rara"]
    assert var["label"] == "Presion Rara"
    assert var["value"] == 1013.25
    assert var["unit"] == "hPa"


def test_history_agrupa_por_variable_y_convierte_viento(client, db_double, mocker):
    conn, cur = db_double
    t1 = datetime(2026, 7, 6, 10, 0, 0)
    t2 = datetime(2026, 7, 6, 10, 10, 0)
    cur.fetchall.return_value = [
        # variable_name, db_unit, ts, raw
        ("Temperatura del Agua", "°C", t1, "5.0"),
        ("Temperatura del Agua", "°C", t2, "5.5"),
        ("Velocidad del Viento", "m/s", t1, "10.0"),
    ]
    mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd0/history")
    body = resp.get_json()

    assert resp.status_code == 200
    assert len(body["water_temperature"]["data"]) == 2
    assert body["water_temperature"]["unit"] == "°C"
    assert body["water_temperature"]["data"][0]["value"] == 5.0

    assert body["wind_speed"]["unit"] == "km/h"
    assert body["wind_speed"]["data"][0]["value"] == 36.0


def test_history_sin_filas_devuelve_diccionario_vacio(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchall.return_value = []
    mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd0/history")

    assert resp.status_code == 200
    assert resp.get_json() == {}
