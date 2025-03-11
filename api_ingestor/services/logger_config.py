import logging
import os
from logging.handlers import RotatingFileHandler

# Configuración de logging
log_dir = "/app/logs/api.log"

# Elimina manejadores previos para evitar duplicados
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Configurar la rotación de logs (5MB por archivo, mantiene 5 archivos antiguos)
file_handler = RotatingFileHandler(log_dir, maxBytes=5 * 1024 * 1024, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


