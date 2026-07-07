"""
Configuración compartida de tests para web_app.

IMPORTANTE: las variables de entorno se setean ANTES de cualquier import de
`config`, `db`, `app`, etc. porque `config.py` crea carpetas (UPLOAD_FOLDER,
EXPORT_DIR) al momento de importarse. Si no se setean acá, los tests
intentarían crear /app/uploads y /app/exports en la máquina que corre pytest.
"""
import os
import sys
import tempfile
from pathlib import Path

WEB_APP_DIR = Path(__file__).resolve().parent.parent
if str(WEB_APP_DIR) not in sys.path:
    sys.path.insert(0, str(WEB_APP_DIR))

_TMP_ROOT = tempfile.mkdtemp(prefix="oogsj_webapp_tests_")
os.environ.setdefault("UPLOAD_FOLDER", os.path.join(_TMP_ROOT, "uploads"))
os.environ.setdefault("EXPORT_DIR", os.path.join(_TMP_ROOT, "exports"))
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_pass")
os.environ.setdefault("JWT_SECRET", "test-secret-key-not-for-prod")
os.environ.setdefault("MAIL_USERNAME", "test@example.com")
os.environ.setdefault("MAIL_PASSWORD", "test-pass")
os.environ.setdefault("SECURE_COOKIES", "false")

import pytest  # noqa: E402


@pytest.fixture()
def app():
    """Instancia nueva de la app por test (create_app() es una factory limpia)."""
    from app import create_app
    application = create_app()
    application.config.update(TESTING=True)
    return application


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_double(mocker):
    """
    Doble de conexión psycopg2: conn.cursor() -> cur reutilizable.
    Uso en un test:
        conn, cur = db_double
        cur.fetchall.return_value = [...]
        mocker.patch("blueprints.emac_cmd0_bp.get_db_connection", return_value=conn)
    """
    conn = mocker.MagicMock(name="conn")
    cur = mocker.MagicMock(name="cursor")
    conn.cursor.return_value = cur
    return conn, cur


@pytest.fixture()
def admin_viewer_cookie():
    """JWT válido de un admin con rol 'viewer' (pasa admin_required, falla master_required)."""
    from core_auth import create_jwt
    return create_jwt({
        "uid": 1, "email": "viewer@test.com",
        "is_admin": True, "admin_role": "viewer",
    })


@pytest.fixture()
def admin_master_cookie():
    """JWT válido de un admin con rol 'master' (pasa admin_required y master_required)."""
    from core_auth import create_jwt
    return create_jwt({
        "uid": 2, "email": "master@test.com",
        "is_admin": True, "admin_role": "master",
    })


@pytest.fixture()
def non_admin_cookie():
    """JWT válido pero de un usuario sin permisos de admin."""
    from core_auth import create_jwt
    return create_jwt({
        "uid": 3, "email": "user@test.com",
        "is_admin": False, "admin_role": None,
    })
