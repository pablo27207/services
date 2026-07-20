"""
Tests de web_app/blueprints/admin_bp.py — dashboard de administración.

Cubre autenticación (admin_required / master_required vía cookie JWT) y la
lógica de cálculo de "estado" de cada plataforma (ok / alerta / sin_datos),
que es pura lógica de fechas fácil de romper sin darse cuenta.
"""
from datetime import datetime, timedelta

import pytest


# ── Autenticación ────────────────────────────────────────────────────────────

def test_stats_sin_cookie_devuelve_401(client):
    resp = client.get("/api/admin/stats")
    assert resp.status_code == 401


def test_stats_con_usuario_no_admin_devuelve_401(client, non_admin_cookie):
    client.set_cookie("auth_token", non_admin_cookie)
    resp = client.get("/api/admin/stats")
    assert resp.status_code == 401


def test_plataformas_con_admin_viewer_devuelve_200(client, admin_viewer_cookie, db_double, mocker):
    conn, cur = db_double
    cur.fetchall.side_effect = [[], []]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/plataformas")

    assert resp.status_code == 200


def test_mantenimiento_patch_requiere_rol_master_no_solo_admin(client, admin_viewer_cookie):
    """Un admin 'viewer' no debe poder activar mantenimiento (solo 'master')."""
    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.patch("/api/admin/plataformas/1/mantenimiento", json={"maintenance_mode": True})
    assert resp.status_code == 403


def test_mantenimiento_patch_con_master_devuelve_200(client, admin_master_cookie, db_double, mocker):
    conn, cur = db_double
    cur.fetchone.return_value = (1, "Boya CIDMAR-2", True, "Reparación de sensores")
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_master_cookie)
    resp = client.patch(
        "/api/admin/plataformas/1/mantenimiento",
        json={"maintenance_mode": True, "maintenance_message": "Reparación de sensores"},
    )
    body = resp.get_json()

    assert resp.status_code == 200
    assert body["en_mantenimiento"] is True
    conn.commit.assert_called_once()


def test_mantenimiento_patch_plataforma_inexistente_devuelve_404(client, admin_master_cookie, db_double, mocker):
    conn, cur = db_double
    cur.fetchone.return_value = None
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_master_cookie)
    resp = client.patch("/api/admin/plataformas/9999/mantenimiento", json={"maintenance_mode": True})

    assert resp.status_code == 404


# ── /api/admin/stats: agregación ─────────────────────────────────────────────

def test_stats_agrega_correctamente(client, admin_viewer_cookie, db_double, mocker):
    conn, cur = db_double
    ultima_medicion = datetime(2026, 7, 6, 10, 0, 0)
    cur.fetchone.side_effect = [
        (1000, 50, 5, ultima_medicion),   # mediciones
        (7,),                              # plataformas activas
        (20, 3),                           # avisos
        (42,),                             # documentos
        ("123/26", datetime(2026, 7, 1).date(), datetime(2026, 7, 1, 12)),  # ultimo aviso
    ]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/stats")
    body = resp.get_json()

    assert resp.status_code == 200
    assert body["mediciones"]["total"] == 1000
    assert body["plataformas_activas"] == 7
    assert body["avisos"]["total"] == 20
    assert body["documentos"] == 42
    assert body["avisos"]["ultimo"]["numero"] == "123/26"


# ── /api/admin/plataformas: cálculo de estado por antigüedad de datos ───────

def test_plataforma_con_datos_recientes_esta_ok(client, admin_viewer_cookie, db_double, mocker):
    """
    Nota: los horarios se calculan relativos a datetime.utcnow() real (no se usa
    freeze_time acá) porque el JWT de autenticación se firma con la hora real al
    crear la cookie, y congelar el reloj lo deja "todavía no válido" (iat en el
    futuro respecto al reloj congelado) -> PyJWT lo rechaza con 401.
    """
    conn, cur = db_double
    ultima_ts = datetime.utcnow() - timedelta(hours=1)
    cur.fetchall.side_effect = [
        [(1, "Boya", "Boya Oceanográfica", False, None, 5, ultima_ts, 100, 10)],
        [(1, "Sensor A")],
    ]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/plataformas")
    plat = resp.get_json()["plataformas"][0]

    assert plat["estado"] == "ok"
    assert plat["horas_sin_datos"] == pytest.approx(1.0, abs=0.05)


def test_plataforma_con_20h_sin_datos_esta_en_alerta(client, admin_viewer_cookie, db_double, mocker):
    conn, cur = db_double
    ultima_ts = datetime.utcnow() - timedelta(hours=20)
    cur.fetchall.side_effect = [
        [(1, "APPCR Puerto CR", "Estación Meteorológica", False, None, 5, ultima_ts, 100, 0)],
        [(1, "Sensor A")],
    ]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/plataformas")
    plat = resp.get_json()["plataformas"][0]

    assert plat["estado"] == "alerta"


def test_plataforma_con_50h_sin_datos_esta_sin_datos(client, admin_viewer_cookie, db_double, mocker):
    conn, cur = db_double
    ultima_ts = datetime.utcnow() - timedelta(hours=50)
    cur.fetchall.side_effect = [
        [(1, "APPCR Muelle CC", "Estación Meteorológica", True, "En reparación", 5, ultima_ts, 100, 0)],
        [(1, "Sensor A")],
    ]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/plataformas")
    plat = resp.get_json()["plataformas"][0]

    assert plat["estado"] == "sin_datos"
    assert plat["en_mantenimiento"] is True


def test_plataforma_con_timestamp_futuro_esta_ok_sin_horas(client, admin_viewer_cookie, db_double, mocker):
    """Predicción de marea: timestamps a futuro no deben marcarse como 'sin_datos'."""
    conn, cur = db_double
    ultima_ts = datetime.utcnow() + timedelta(hours=24)
    cur.fetchall.side_effect = [
        [(2, "Predicción de Marea", "Modelo Numérico", False, None, 2, ultima_ts, 1000, 100)],
        [(2, "Sensor A")],
    ]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/plataformas")
    plat = resp.get_json()["plataformas"][0]

    assert plat["estado"] == "ok"
    assert plat["horas_sin_datos"] is None


def test_plataforma_sin_ninguna_medicion_esta_sin_datos(client, admin_viewer_cookie, db_double, mocker):
    conn, cur = db_double
    cur.fetchall.side_effect = [
        [(5, "APPCR Muelle CC", "Estación Meteorológica", True, "Sin conexión", 82, None, 0, 0)],
        [(5, "Sensor A")],
    ]
    mocker.patch("blueprints.admin_bp.get_db_connection", return_value=conn)

    client.set_cookie("auth_token", admin_viewer_cookie)
    resp = client.get("/api/admin/plataformas")
    plat = resp.get_json()["plataformas"][0]

    assert plat["estado"] == "sin_datos"
    assert plat["ultima_transmision"] is None
