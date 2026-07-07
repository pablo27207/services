"""
Tests de services/emac_cmd1_scraper.py — estructuralmente idéntico a
emac_cmd0_scraper.py (ver test_emac_cmd0_scraper.py), pero se testea aparte
porque es un módulo independiente: un bug introducido solo en este archivo
(ej. al copiar/pegar desde CMD0) no lo detectaría la suite de CMD0.
"""
import requests
import pytest

from services.emac_cmd1_scraper import EMACCMD1Scraper, _resolve_ids


def _conn_con(sensor_rows, location_row):
    import unittest.mock as mock
    conn = mock.MagicMock()
    cur = mock.MagicMock()
    conn.cursor.return_value = cur
    cur.fetchall.return_value = sensor_rows
    cur.fetchone.return_value = location_row
    return conn


def _csv_response(text, raise_error=None):
    import unittest.mock as mock
    resp = mock.MagicMock()
    resp.text = text
    if raise_error:
        resp.raise_for_status.side_effect = raise_error
    else:
        resp.raise_for_status.return_value = None
    return resp


def test_resolve_ids_sin_sensores_lanza_runtime_error_con_pista_de_migracion(mocker):
    mocker.patch(
        "services.emac_cmd1_scraper.psycopg2.connect",
        return_value=_conn_con([], None),
    )
    with pytest.raises(RuntimeError, match="20260701_add_emac_cmd1_station"):
        _resolve_ids()


def test_resolve_ids_sin_location_activa_lanza_runtime_error(mocker):
    mocker.patch(
        "services.emac_cmd1_scraper.psycopg2.connect",
        return_value=_conn_con([("Sensor de Nivel del Agua - CMD1", 203)], None),
    )
    with pytest.raises(RuntimeError, match="location activa"):
        _resolve_ids()


def test_resolve_ids_mapea_los_6_sensores_esperados(mocker):
    sensores = [
        ("Sensor de Nivel del Agua - CMD1", 203),
        ("Sensor de Temperatura del Agua - CMD1", 204),
        ("Sensor de Conductividad - CMD1", 205),
        ("Sensor de Temperatura del Aire - CMD1", 206),
        ("Sensor de Velocidad del Viento - CMD1", 207),
        ("Sensor de Dirección del Viento - CMD1", 208),
    ]
    mocker.patch(
        "services.emac_cmd1_scraper.psycopg2.connect",
        return_value=_conn_con(sensores, (12,)),
    )

    variables, location_id = _resolve_ids()

    assert location_id == 12
    assert set(variables.keys()) == {"16", "13", "17", "05", "03", "02"}
    assert variables["16"][0] == 203
    assert variables["03"][0] == 207


def test_fetch_station_data_sin_ids_resueltos_devuelve_lista_vacia(mocker):
    mocker.patch(
        "services.emac_cmd1_scraper._resolve_ids",
        side_effect=RuntimeError("migración no aplicada"),
    )
    assert EMACCMD1Scraper.fetch_station_data() == []


def test_fetch_station_data_convierte_viento_de_kmh_a_ms(mocker):
    mocker.patch(
        "services.emac_cmd1_scraper._resolve_ids",
        return_value=({"03": (207, lambda v: v / 3.6)}, 12),
    )
    csv = "ts,val\n2026-07-06 10:40:00,50.0\n"
    mocker.patch("services.emac_cmd1_scraper.requests.get", return_value=_csv_response(csv))

    resultados = EMACCMD1Scraper.fetch_station_data()

    assert resultados[0][1] == pytest.approx(50.0 / 3.6)
    assert resultados[0][4] == 207
    assert resultados[0][5] == 12


def test_fetch_station_data_descarta_filas_invalidas(mocker):
    mocker.patch(
        "services.emac_cmd1_scraper._resolve_ids",
        return_value=({"16": (203, None)}, 12),
    )
    csv = "ts,val\nfecha-mala,5\n2026-07-06 10:40:00,8.13\n"
    mocker.patch("services.emac_cmd1_scraper.requests.get", return_value=_csv_response(csv))

    resultados = EMACCMD1Scraper.fetch_station_data()

    assert len(resultados) == 1
    assert resultados[0][1] == 8.13


def test_fetch_station_data_una_variable_sin_datos_no_bloquea_las_demas(mocker):
    """
    Regresión directa a lo observado en producción hoy: 'Nivel del Agua' y
    'Conductividad' vinieron sin datos válidos tras el parseo, pero las
    otras 4 variables sí debían insertarse igual.
    """
    mocker.patch(
        "services.emac_cmd1_scraper._resolve_ids",
        return_value=({"16": (203, None), "05": (206, None)}, 12),
    )

    def fake_get(url, timeout):
        if "var_code=16" in url:
            return _csv_response("ts,val\nfecha-invalida,no-numero\n")  # todo NaN tras el parseo
        return _csv_response("ts,val\n2026-07-06 10:40:00,10.19\n")

    mocker.patch("services.emac_cmd1_scraper.requests.get", side_effect=fake_get)

    resultados = EMACCMD1Scraper.fetch_station_data()

    assert len(resultados) == 1
    assert resultados[0][4] == 206  # solo la variable con datos válidos


def test_fetch_station_data_request_exception_generica_no_rompe(mocker):
    mocker.patch(
        "services.emac_cmd1_scraper._resolve_ids",
        return_value=({"16": (203, None)}, 12),
    )
    mocker.patch(
        "services.emac_cmd1_scraper.requests.get",
        side_effect=requests.exceptions.ConnectionError("DNS falló"),
    )

    assert EMACCMD1Scraper.fetch_station_data() == []
