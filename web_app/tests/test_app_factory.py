"""
Tests de arranque de la aplicación (web_app/app.py).

Estos son los tests más baratos y más valiosos de correr antes de cada
deploy: si create_app() explota, o si dos blueprints chocan de ruta,
TODA la API cae en producción. Deben correr en segundos y sin DB real.
"""
import pytest


EXPECTED_BLUEPRINTS = {
    "auth", "ocean", "stations", "library", "contact", "files",
    "avisos", "admin", "noticias", "especies", "exports",
    "emac_cmd0", "emac_cmd1", "users",
}


def test_create_app_no_explota():
    from app import create_app
    app = create_app()
    assert app is not None


def test_todos_los_blueprints_esperados_estan_registrados():
    from app import create_app
    app = create_app()
    registrados = set(app.blueprints.keys())
    faltantes = EXPECTED_BLUEPRINTS - registrados
    assert not faltantes, f"Blueprints esperados que no se registraron: {faltantes}"


def test_no_hay_rutas_duplicadas_entre_blueprints():
    """
    Regresión genérica: si dos blueprints registran el mismo (path, método),
    Flask deja la última definición y la otra queda inalcanzable en silencio.
    Esto es exactamente lo que casi pasa entre EMAC CMD0 y CMD1 si hubiesen
    compartido url_prefix.
    """
    from app import create_app
    app = create_app()

    vistos = {}
    for rule in app.url_map.iter_rules():
        metodos = rule.methods - {"HEAD", "OPTIONS"}
        for metodo in metodos:
            clave = (rule.rule, metodo)
            assert clave not in vistos, (
                f"Ruta duplicada {clave}: ya registrada por endpoint "
                f"'{vistos[clave]}', también reclamada por '{rule.endpoint}'"
            )
            vistos[clave] = rule.endpoint


@pytest.mark.parametrize("nombre_bp,prefix_esperado", [
    ("emac_cmd0", "/api/emac_cmd0"),
    ("emac_cmd1", "/api/emac_cmd1"),
])
def test_prefijos_emac_no_colisionan(nombre_bp, prefix_esperado):
    """
    Regresión directa al riesgo real de esta sesión: CMD0 y CMD1 deben vivir
    bajo prefijos completamente distintos, si no uno pisa las rutas del otro.
    """
    from app import create_app
    app = create_app()
    assert app.blueprints[nombre_bp].url_prefix == prefix_esperado


def test_health_responde_ok():
    """/health está atado a la instancia global `app`, no a create_app()."""
    import app as app_module
    client = app_module.app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}
