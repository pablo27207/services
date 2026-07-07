"""
Tests de web_app/blueprints/ocean_bp.py — mareógrafo, boya, predicción de marea.
"""
from datetime import datetime


def test_mareograph_devuelve_lista_de_niveles(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 8, 0, 0)
    cur.fetchall.return_value = [(ts, "2.34")]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/mareograph")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body[0]["level"] == 2.34


def test_mareograph_latest_agrupa_por_sensor(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 8, 0, 0)
    cur.fetchall.return_value = [("Nivel del Mar", ts.isoformat(), "1.5", "m")]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/mareograph/latest")
    body = resp.get_json()

    assert body["Nivel del Mar"]["value"] == 1.5
    assert body["Nivel del Mar"]["unit"] == "m"


def test_mareograph_latest_con_valor_none(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchall.return_value = [("Nivel del Mar", None, None, "m")]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/mareograph/latest")
    body = resp.get_json()

    assert body["Nivel del Mar"]["value"] is None


def test_buoy_agrupa_todas_las_variables_conocidas_aunque_sin_datos(client, db_double, mocker):
    """Todas las variables de BUOY_SENSORS deben estar presentes, aunque vacías."""
    conn, cur = db_double
    cur.fetchall.return_value = []
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/buoy")
    body = resp.get_json()

    for nombre in ["Altura de Olas", "Periodo de Olas", "Dirección de Olas",
                   "Velocidad de Corriente", "Dirección de la Corriente",
                   "Radiación PAR", "Batería"]:
        assert nombre in body
        assert body[nombre] == []


def test_buoy_con_sensor_desconocido_usa_fallback(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 8, 0, 0)
    cur.fetchall.return_value = [(999, ts, 5.0)]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/buoy")
    body = resp.get_json()

    assert "Sensor 999" in body
    assert body["Sensor 999"][0]["value"] == 5.0


def test_buoy_latest(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 8, 0, 0)
    cur.fetchall.return_value = [("Altura de Olas", ts.isoformat(), "1.2", "m")]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/buoy/latest")
    body = resp.get_json()

    assert body["Altura de Olas"]["value"] == 1.2


def test_tide_forecast_devuelve_niveles(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 8, 0, 0)
    cur.fetchall.return_value = [(ts, "1.85")]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/tide_forecast")
    body = resp.get_json()

    assert body[0]["level"] == 1.85


def test_plataforma_estado_encontrada(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchone.return_value = (True, "En mantenimiento")
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/plataforma/6/estado")
    body = resp.get_json()

    assert body == {"en_mantenimiento": True, "mensaje": "En mantenimiento"}


def test_plataforma_estado_no_encontrada(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchone.return_value = None
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/plataforma/9999/estado")
    body = resp.get_json()

    assert body == {"en_mantenimiento": False, "mensaje": None}


def test_plataforma_estado_rechaza_id_no_numerico(client):
    """La ruta usa <int:platform_id>, un id no numérico debe dar 404 (no 500)."""
    resp = client.get("/api/plataforma/abc/estado")
    assert resp.status_code == 404


def test_mediciones_negativas_serializa_timestamp(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 8, 0, 0)
    cur.fetchall.return_value = [("Sensor X", -5.2, ts, "m")]
    mocker.patch("blueprints.ocean_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/mediciones_negativas")
    body = resp.get_json()

    assert body[0]["sensor"] == "Sensor X"
    assert body[0]["valor"] == -5.2
    assert body[0]["timestamp"] == ts.isoformat()
    assert body[0]["unidad"] == "m"
