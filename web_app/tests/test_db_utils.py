"""
Tests de web_app/db.py — safe_float().

safe_float se usa en ocean_bp para convertir valores crudos de la DB antes de
devolverlos por API. Si se rompe, todos los endpoints de mareógrafo/boya
devuelven basura o explotan.
"""
from db import safe_float


def test_safe_float_con_numero_valido_string():
    assert safe_float("3.14") == 3.14


def test_safe_float_con_int():
    assert safe_float(5) == 5.0


def test_safe_float_con_none_devuelve_cero():
    assert safe_float(None) == 0.0


def test_safe_float_con_string_invalido_devuelve_cero():
    assert safe_float("no-es-un-numero") == 0.0


def test_safe_float_con_nan_devuelve_cero():
    assert safe_float(float("nan")) == 0.0


def test_safe_float_con_infinito_no_se_normaliza():
    """
    Caso borde documentado: math.isnan(inf) es False, así que safe_float
    NO convierte infinito a 0.0 (a diferencia de NaN). Si algún día se
    "corrige" esto sin querer, este test debe fallar y avisar.
    """
    assert safe_float(float("inf")) == float("inf")


def test_safe_float_con_lista_devuelve_cero():
    assert safe_float([1, 2, 3]) == 0.0
