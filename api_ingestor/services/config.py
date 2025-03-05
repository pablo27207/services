import os
import sys

# Función para obtener variables de entorno y fallar si no están definidas
def get_env_var(var_name):
    value = os.getenv(var_name)
    if value is None:
        print(f"❌ ERROR: La variable de entorno {var_name} no está definida.")
        sys.exit(1)  # Termina la ejecución con código de error 1
    return value

DB_CONFIG = {
    "dbname": get_env_var("POSTGRES_DB"),
    "user": get_env_var("POSTGRES_USER"),
    "password": get_env_var("POSTGRES_PASSWORD"),
    "host": get_env_var("POSTGRES_HOST"),
    "port": get_env_var("POSTGRES_PORT"),
}
