import math
import psycopg2
from config import DB_CONFIG


def get_db_connection():
    """Retorna una conexión psycopg2. El caller es responsable de cerrarla."""
    return psycopg2.connect(**DB_CONFIG)


def safe_float(val):
    """Convierte val a float, devuelve 0.0 si es NaN o inválido."""
    try:
        f = float(val)
        return f if not math.isnan(f) else 0.0
    except Exception:
        return 0.0