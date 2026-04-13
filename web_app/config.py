import os
from pathlib import Path

# ── Base de datos ──────────────────────────────────────────
DB_CONFIG = {
    "dbname":   os.getenv("POSTGRES_DB"),
    "user":     os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host":     "db",
    "port":     5432,
}

# ── JWT ────────────────────────────────────────────────────
JWT_SECRET      = os.getenv("JWT_SECRET", "cambia-esta-clave")
JWT_ISS         = "oogsj-auth"
JWT_EXP_MIN     = 120
SECURE_COOKIES  = os.getenv("SECURE_COOKIES", "false").lower() == "true"

# ── Uploads ────────────────────────────────────────────────
UPLOAD_FOLDER   = os.getenv("UPLOAD_FOLDER", "/app/uploads")
ALLOWED_MIMES   = {"application/pdf"}
MAX_UPLOAD_BYTES = 50 * 1024 * 1024  # 50 MB

# Crear carpeta si no existe
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# ── Mail ───────────────────────────────────────────────────
MAIL_SERVER         = os.getenv("MAIL_SERVER", "smtp.gmail.com")
MAIL_PORT           = int(os.getenv("MAIL_PORT", 587))
MAIL_USE_TLS        = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
MAIL_USERNAME       = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD       = os.getenv("MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)