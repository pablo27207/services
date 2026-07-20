"""
Tests de web_app/blueprints/emac_cmd1_bp.py — estación EMAC Club Náutico (CMD1).

Mismo contrato que CMD0 (ver test_emac_cmd0_bp.py) más un endpoint extra:
  - GET /api/emac_cmd1/estado    (estado de mantenimiento por nombre de plataforma)
"""
from datetime import datetime


def test_get_data_sin_filas_devuelve_estructura_vacia(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchall.return_value = []
    mocker.patch("blueprints.emac_cmd1_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd1/")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body == {
        "station_code": "emac_cmd1",
        "station_name": "Estación EMAC - CMD1",
        "timestamp": None,
        "variables": {},
    }


def test_get_data_con_filas_convierte_viento_a_kmh(client, db_double, mocker):
    conn, cur = db_double
    ts = datetime(2026, 7, 6, 10, 40, 0)
    cur.fetchall.return_value = [
        (207, "Sensor de Velocidad del Viento - CMD1", "Velocidad del Viento", "m/s", ts, "3.861"),
    ]
    mocker.patch("blueprints.emac_cmd1_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd1/")
    body = resp.get_json()

    assert body["variables"]["wind_speed"]["value"] == 13.9  # 3.861 * 3.6 redondeado
    assert body["variables"]["wind_speed"]["unit"] == "km/h"


def test_history_agrupa_por_variable(client, db_double, mocker):
    conn, cur = db_double
    t1 = datetime(2026, 7, 6, 10, 0, 0)
    cur.fetchall.return_value = [
        ("Dirección del Viento", "°", t1, "247.5"),
    ]
    mocker.patch("blueprints.emac_cmd1_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd1/history")
    body = resp.get_json()

    assert body["wind_direction"]["unit"] == "°"
    assert body["wind_direction"]["data"][0]["value"] == 247.5


def test_estado_plataforma_en_mantenimiento(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchone.return_value = (True, "Mantenimiento programado por lluvia")
    mocker.patch("blueprints.emac_cmd1_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd1/estado")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body == {"en_mantenimiento": True, "mensaje": "Mantenimiento programado por lluvia"}


def test_estado_plataforma_activa(client, db_double, mocker):
    conn, cur = db_double
    cur.fetchone.return_value = (False, None)
    mocker.patch("blueprints.emac_cmd1_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd1/estado")
    assert resp.get_json() == {"en_mantenimiento": False, "mensaje": None}


def test_estado_plataforma_inexistente_no_falla(client, db_double, mocker):
    """
    Regresión directa al bug de esta sesión: si la migración de CMD1 no corrió
    todavía, la plataforma no existe en la DB. El endpoint no debe romper,
    debe responder "no en mantenimiento" por defecto.
    """
    conn, cur = db_double
    cur.fetchone.return_value = None
    mocker.patch("blueprints.emac_cmd1_bp.get_db_connection", return_value=conn)

    resp = client.get("/api/emac_cmd1/estado")

    assert resp.status_code == 200
    assert resp.get_json() == {"en_mantenimiento": False, "mensaje": None}
