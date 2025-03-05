import logging
import os
from logging.handlers import RotatingFileHandler

# Configuración de logging
log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)

# Detectar si estamos en un worker de Celery
is_celery = os.getenv("CELERY_WORKER") == "true"

# Seleccionar el archivo de logs correcto
log_file = os.path.join(log_dir, "celery.log" if is_celery else "api.log")

# Elimina manejadores previos para evitar duplicados
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configurar la rotación de logs (5MB por archivo, mantiene 5 archivos antiguos)
file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


