"""
Tests de celery_tasks.py — la fábrica genérica que envuelve cada scraper en
una tarea Celery (create_celery_task) y persiste sus resultados con DBHandler.

Las tareas se invocan con `.run()` para ejecutarlas de forma síncrona, sin
necesitar un broker Redis real ni un worker corriendo.
"""
import pytest

import celery_tasks


def test_task_exitosa_llama_al_scraper_e_inserta_measurements(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch("celery_tasks.DBHandler", return_value=mock_db)
    scraper = mocker.MagicMock(return_value=[("fila1",), ("fila2",)])

    task = celery_tasks.create_celery_task("tarea_de_prueba", scraper)
    resultado = task.run()

    scraper.assert_called_once()
    mock_db.insert_measurements.assert_called_once_with([("fila1",), ("fila2",)])
    mock_db.insert_avisos.assert_not_called()
    assert resultado == {"status": "success", "records": 2}


def test_task_de_avisos_usa_insert_avisos_no_insert_measurements(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch("celery_tasks.DBHandler", return_value=mock_db)
    scraper = mocker.MagicMock(return_value=[("aviso1",)])

    task = celery_tasks.create_celery_task("shn_avisos", scraper)
    task.run()

    mock_db.insert_avisos.assert_called_once_with([("aviso1",)])
    mock_db.insert_measurements.assert_not_called()


def test_task_con_datos_vacios_no_llama_a_insert_measurements(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch("celery_tasks.DBHandler", return_value=mock_db)
    scraper = mocker.MagicMock(return_value=[])

    task = celery_tasks.create_celery_task("tarea_vacia", scraper)

    with pytest.raises(Exception):
        task.run()

    mock_db.insert_measurements.assert_not_called()


def test_task_propaga_si_el_scraper_lanza_excepcion(mocker):
    mocker.patch("celery_tasks.DBHandler")
    scraper = mocker.MagicMock(side_effect=ValueError("fuente caída"))

    task = celery_tasks.create_celery_task("tarea_rota", scraper)

    with pytest.raises(Exception):
        task.run()


def test_emac_cmd0_y_cmd1_quedan_registradas_como_tareas_celery():
    """
    Regresión directa a la sesión de hoy: task_config.py define las entradas,
    pero si celery_tasks.py no las recorre bien, la tarea nunca se registra
    en Celery y el beat nunca la dispara aunque exista en TASKS.
    """
    nombres_registrados = set(celery_tasks.app.tasks.keys())
    assert "celery_tasks.fetch_emac_cmd0_station" in nombres_registrados
    assert "celery_tasks.fetch_emac_cmd1_station" in nombres_registrados


def test_beat_schedule_incluye_emac_cmd0_y_cmd1():
    schedule = celery_tasks.app.conf.beat_schedule
    assert "emac_cmd0_station" in schedule
    assert "emac_cmd1_station" in schedule
    assert schedule["emac_cmd0_station"]["task"] == "celery_tasks.fetch_emac_cmd0_station"
    assert schedule["emac_cmd1_station"]["task"] == "celery_tasks.fetch_emac_cmd1_station"
