"""
Tests de services/emac_cmd0_scraper.py.

Cubre:
  - _resolve_ids(): mapeo de sensores desde la DB, y sus errores esperados
    cuando la migración no fue aplicada (plataforma/location inexistente).
  - fetch_station_data(): parseo del CSV de la API EMAC, conversión de
    unidades (viento km/h -> m/s), y que un error en una variable no tumbe
    el resto del loop.
"""
import requests
import pytest

from services.emac_cmd0_scraper import EMACCMD0Scraper, _resolve_ids


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


# ── _resolve_ids ─────────────────────────────────────────────────────────────

def test_resolve_ids_sin_sensores_lanza_runtime_error_con_pista_de_migracion(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper.psycopg2.connect",
        return_value=_conn_con([], None),
    )
    with pytest.raises(RuntimeError, match="20260601_add_emac_cmd0_station"):
        _resolve_ids()


def test_resolve_ids_sin_location_activa_lanza_runtime_error(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper.psycopg2.connect",
        return_value=_conn_con([("Sensor de Nivel del Agua - CMD0", 10)], None),
    )
    with pytest.raises(RuntimeError, match="location activa"):
        _resolve_ids()


def test_resolve_ids_ignora_sensores_no_mapeados(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper.psycopg2.connect",
        return_value=_conn_con(
            [
                ("Sensor de Nivel del Agua - CMD0", 10),
                ("Sensor de Otra Estación Sin Relación", 999),
            ],
            (7,),
        ),
    )
    variables, location_id = _resolve_ids()

    assert location_id == 7
    assert list(variables.keys()) == ["16"]
    assert variables["16"][0] == 10


def test_resolve_ids_cierra_conexion_y_cursor_siempre(mocker):
    conn = _conn_con([("Sensor de Nivel del Agua - CMD0", 10)], (7,))
    mocker.patch("services.emac_cmd0_scraper.psycopg2.connect", return_value=conn)

    _resolve_ids()

    conn.cursor.return_value.close.assert_called_once()
    conn.close.assert_called_once()


# ── fetch_station_data ───────────────────────────────────────────────────────

def test_fetch_station_data_sin_ids_resueltos_devuelve_lista_vacia(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        side_effect=RuntimeError("migración no aplicada"),
    )
    assert EMACCMD0Scraper.fetch_station_data() == []


def test_fetch_station_data_parsea_y_arma_tuplas_correctamente(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"16": (10, None)}, 5),
    )
    csv = "ts,val\n2026-07-06 10:00:00,1.23\n2026-07-06 10:10:00,1.30\n"
    mocker.patch("services.emac_cmd0_scraper.requests.get", return_value=_csv_response(csv))

    resultados = EMACCMD0Scraper.fetch_station_data()

    assert len(resultados) == 2
    ts, value, quality, level, sensor_id, location_id = resultados[0]
    assert value == 1.23
    assert quality == 1
    assert level == 1
    assert sensor_id == 10
    assert location_id == 5


def test_fetch_station_data_convierte_viento_de_kmh_a_ms(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"03": (11, lambda v: v / 3.6)}, 5),
    )
    csv = "ts,val\n2026-07-06 10:00:00,36.0\n"
    mocker.patch("services.emac_cmd0_scraper.requests.get", return_value=_csv_response(csv))

    resultados = EMACCMD0Scraper.fetch_station_data()

    assert resultados[0][1] == pytest.approx(10.0)


def test_fetch_station_data_descarta_filas_con_timestamp_o_valor_invalido(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"16": (10, None)}, 5),
    )
    csv = "ts,val\nno-es-fecha,no-es-numero\n2026-07-06 10:00:00,1.23\n"
    mocker.patch("services.emac_cmd0_scraper.requests.get", return_value=_csv_response(csv))

    resultados = EMACCMD0Scraper.fetch_station_data()

    assert len(resultados) == 1
    assert resultados[0][1] == 1.23


def test_fetch_station_data_respuesta_vacia_no_agrega_nada(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"16": (10, None)}, 5),
    )
    mocker.patch("services.emac_cmd0_scraper.requests.get", return_value=_csv_response("   "))

    assert EMACCMD0Scraper.fetch_station_data() == []


def test_fetch_station_data_csv_con_una_sola_columna_no_rompe(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"16": (10, None)}, 5),
    )
    mocker.patch("services.emac_cmd0_scraper.requests.get", return_value=_csv_response("solo_una_columna\nabc\n"))

    assert EMACCMD0Scraper.fetch_station_data() == []


def test_fetch_station_data_timeout_en_una_variable_no_corta_las_demas(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"16": (10, None), "13": (11, None)}, 5),
    )
    csv_ok = "ts,val\n2026-07-06 10:00:00,5.0\n"

    def fake_get(url, timeout):
        if "var_code=16" in url:
            raise requests.exceptions.Timeout()
        return _csv_response(csv_ok)

    mocker.patch("services.emac_cmd0_scraper.requests.get", side_effect=fake_get)

    resultados = EMACCMD0Scraper.fetch_station_data()

    assert len(resultados) == 1
    assert resultados[0][4] == 11  # sensor_id de la variable que sí funcionó


def test_fetch_station_data_http_error_en_una_variable_no_corta_las_demas(mocker):
    mocker.patch(
        "services.emac_cmd0_scraper._resolve_ids",
        return_value=({"16": (10, None), "13": (11, None)}, 5),
    )
    csv_ok = "ts,val\n2026-07-06 10:00:00,5.0\n"

    def fake_get(url, timeout):
        if "var_code=16" in url:
            return _csv_response("", raise_error=requests.exceptions.HTTPError("500"))
        return _csv_response(csv_ok)

    mocker.patch("services.emac_cmd0_scraper.requests.get", side_effect=fake_get)

    resultados = EMACCMD0Scraper.fetch_station_data()

    assert len(resultados) == 1
    assert resultados[0][4] == 11
