"""
Tests de services/db_handler.py — capa de escritura a Postgres usada por
TODAS las tareas Celery vía celery_tasks.py.
"""
import services.db_handler as db_handler_module
from services.db_handler import DBHandler


def _make_handler_with_mock_conn(mocker):
    """Crea un DBHandler sorteando su __init__ real (que abre una conexión real)."""
    handler = DBHandler.__new__(DBHandler)
    handler.conn = mocker.MagicMock()
    handler.cur = mocker.MagicMock()
    return handler


def test_init_si_falla_la_conexion_no_propaga_excepcion(mocker):
    """
    Regresión: DBHandler() nunca debe lanzar, ni siquiera sin DB disponible,
    porque lo instancian las tareas Celery sin try/except alrededor.
    """
    mocker.patch.object(db_handler_module.psycopg2, "connect", side_effect=Exception("DB caída"))

    handler = DBHandler()

    assert handler.conn is None
    assert handler.cur is None


def test_insert_measurements_con_conexion_activa_hace_commit(mocker):
    handler = _make_handler_with_mock_conn(mocker)
    mock_execute_values = mocker.patch.object(db_handler_module, "execute_values")

    handler.insert_measurements([("dato1",), ("dato2",)])

    mock_execute_values.assert_called_once()
    handler.conn.commit.assert_called_once()


def test_insert_measurements_sin_conexion_activa_no_opera(mocker):
    handler = DBHandler.__new__(DBHandler)
    handler.conn = None
    handler.cur = None
    mock_execute_values = mocker.patch.object(db_handler_module, "execute_values")

    handler.insert_measurements([("dato1",)])

    mock_execute_values.assert_not_called()


def test_insert_measurements_si_falla_no_propaga_excepcion(mocker):
    """
    Documenta el comportamiento actual: si execute_values falla, el error se
    loguea pero NO se hace rollback (a diferencia de insert_avisos). Si esto
    cambia sin querer, este test debe fallar y forzar la revisión.
    """
    handler = _make_handler_with_mock_conn(mocker)
    mocker.patch.object(db_handler_module, "execute_values", side_effect=Exception("constraint violada"))

    handler.insert_measurements([("dato1",)])  # no debe lanzar

    handler.conn.rollback.assert_not_called()


def test_insert_avisos_con_lista_vacia_no_opera(mocker):
    handler = _make_handler_with_mock_conn(mocker)
    mock_execute_values = mocker.patch.object(db_handler_module, "execute_values")

    handler.insert_avisos([])

    mock_execute_values.assert_not_called()


def test_insert_avisos_con_datos_hace_commit(mocker):
    handler = _make_handler_with_mock_conn(mocker)
    mock_execute_values = mocker.patch.object(db_handler_module, "execute_values")

    handler.insert_avisos([("001/26", "2026-07-01", "Navegación", "texto", "text")])

    mock_execute_values.assert_called_once()
    handler.conn.commit.assert_called_once()


def test_insert_avisos_si_falla_hace_rollback(mocker):
    """A diferencia de insert_measurements, insert_avisos SÍ hace rollback ante error."""
    handler = _make_handler_with_mock_conn(mocker)
    mocker.patch.object(db_handler_module, "execute_values", side_effect=Exception("fallo"))

    handler.insert_avisos([("001/26", "2026-07-01", "Navegación", "texto", "text")])

    handler.conn.rollback.assert_called_once()


def test_close_cierra_cursor_y_conexion_si_existen(mocker):
    handler = _make_handler_with_mock_conn(mocker)

    handler.close()

    handler.cur.close.assert_called_once()
    handler.conn.close.assert_called_once()


def test_close_no_rompe_si_conn_y_cur_son_none():
    handler = DBHandler.__new__(DBHandler)
    handler.conn = None
    handler.cur = None

    handler.close()  # no debe lanzar
