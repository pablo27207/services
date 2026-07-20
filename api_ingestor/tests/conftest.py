"""
Configuración compartida de tests para api_ingestor.

CRÍTICO: `services/config.py` llama sys.exit(1) al importarse si faltan las
variables de entorno POSTGRES_*. Como Python cachea imports, hay que setear
esas variables ANTES de que pytest importe cualquier módulo de `services`
(incluso indirectamente, vía `celery_tasks.py` o cualquier scraper). Por eso
esto va al nivel de módulo del conftest, no dentro de un fixture.
"""
import os
import sys
from pathlib import Path

API_INGESTOR_DIR = Path(__file__).resolve().parent.parent
if str(API_INGESTOR_DIR) not in sys.path:
    sys.path.insert(0, str(API_INGESTOR_DIR))

os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_pass")
os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")

import pytest  # noqa: E402


@pytest.fixture()
def db_double(mocker):
    """Doble de conexión psycopg2 (conn.cursor() -> cur) para mockear psycopg2.connect."""
    conn = mocker.MagicMock(name="conn")
    cur = mocker.MagicMock(name="cursor")
    conn.cursor.return_value = cur
    return conn, cur
