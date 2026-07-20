"""
Tests de services/task_config.py — el registro central de tareas Celery.

Si una entrada de TASKS está mal formada (scraper no invocable, schedule
inválido), celery_tasks.py falla al armar el beat_schedule y TODO el
scheduler de Celery deja de arrancar, tumbando la ingesta de TODAS las
estaciones, no solo la nueva.
"""
from celery.schedules import crontab

from services.task_config import TASKS

ESTACIONES_ESPERADAS = {
    "buoy", "mareograph", "tide_forecast", "comodoro_rivadavia_port",
    "caleta_muelle_dock", "documentos_scraper", "shn_avisos",
    "emac_cmd0_station", "emac_cmd1_station",
}


def test_todas_las_tareas_esperadas_existen():
    faltantes = ESTACIONES_ESPERADAS - set(TASKS.keys())
    assert not faltantes, f"Tareas esperadas ausentes de TASKS: {faltantes}"


def test_cada_tarea_tiene_scraper_invocable():
    for nombre, cfg in TASKS.items():
        assert "scraper" in cfg, f"{nombre} no define 'scraper'"
        assert callable(cfg["scraper"]), f"{nombre}: 'scraper' no es invocable"


def test_cada_tarea_tiene_schedule_crontab_valido():
    for nombre, cfg in TASKS.items():
        assert "schedule" in cfg, f"{nombre} no define 'schedule'"
        assert isinstance(cfg["schedule"], crontab), f"{nombre}: 'schedule' no es un crontab"


def test_emac_cmd0_y_cmd1_corren_cada_30_minutos():
    """Regresión: ambas estaciones EMAC deben tener la misma cadencia (*/30)."""
    assert str(TASKS["emac_cmd0_station"]["schedule"]) == str(TASKS["emac_cmd1_station"]["schedule"])


def test_emac_cmd0_y_cmd1_usan_scrapers_distintos():
    """Si por error ambas entradas apuntaran al mismo scraper, CMD1 nunca se scrapearía."""
    assert TASKS["emac_cmd0_station"]["scraper"] != TASKS["emac_cmd1_station"]["scraper"]
