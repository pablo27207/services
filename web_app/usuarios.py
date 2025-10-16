from flask import Blueprint, request, jsonify
import psycopg2
import os
import hashlib
from datetime import datetime

usuarios_bp = Blueprint('usuarios', __name__)

DB_USERS = {
    "dbname": os.getenv("SCIENCE_DB_NAME"),
    "user": os.getenv("SCIENCE_DB_USER"),
    "password": os.getenv("SCIENCE_DB_PASSWORD"),
    "host": os.getenv("SCIENCE_DB_HOST", "taxonomica_db"),
    "port": int(os.getenv("SCIENCE_DB_PORT", "5432")),
}

def get_db_taxonomia():
    return psycopg2.connect(**DB_USERS)

# ---------- Registro ----------
@usuarios_bp.route("/api/register", methods=["POST"])
def register_user():
    data = request.get_json() or {}

    first_name = (data.get("first_name") or "").strip()
    last_name  = (data.get("last_name")  or "").strip()
    email      = (data.get("email")      or "").strip().lower()
    password   = data.get("password") or ""
    role       = (data.get("role") or "normal").strip().lower()  # 'normal' por defecto
    dob_str    = (data.get("date_of_birth") or "").strip()       # "YYYY-MM-DD" opcional
    studies    = (data.get("academic_studies") or "").strip()    # opcional

    if not (first_name and last_name and email and password):
        return jsonify({"status":"error","message":"Faltan datos obligatorios"}), 400

    date_of_birth = None
    if dob_str:
        try:
            date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"status":"error","message":"Formato de fecha inválido (use YYYY-MM-DD)"}), 400

    pw_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = get_db_taxonomia()
        cur = conn.cursor()
        # Nota: "User" debe ir con comillas por el uso de mayúscula
        cur.execute("""
            INSERT INTO "User" (first_name, last_name, email, password_hash, role, date_of_birth, academic_studies, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
            RETURNING user_id, first_name, last_name, email, role;
        """, (first_name, last_name, email, pw_hash, role, date_of_birth, studies))

        row = cur.fetchone()
        conn.commit()
        cur.close(); conn.close()

        return jsonify({
            "status":"success",
            "user":{
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "role": row[4]
            }
        }), 201

    except psycopg2.errors.UniqueViolation as e:  # email único
        if not conn.closed:
            conn.rollback()
            cur.close(); conn.close()
        return jsonify({"status":"error","message":"Email ya registrado"}), 409
    except Exception as e:
        # log server
        print("❌ register_user:", type(e).__name__, str(e))
        if 'conn' in locals() and not conn.closed:
            conn.rollback()
            cur.close(); conn.close()
        return jsonify({"status":"error","message":"Error de BD"}), 500

# ---------- Login ----------
@usuarios_bp.route("/api/login", methods=["POST"])
def login_user():
    data = request.get_json() or {}
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not (email and password):
        return jsonify({"status":"error","message":"Faltan credenciales"}), 400

    pw_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = get_db_taxonomia()
        cur = conn.cursor()
        cur.execute("""
            SELECT user_id, first_name, last_name, email, role
            FROM "User"
            WHERE email = %s AND password_hash = %s AND is_active = TRUE;
        """, (email, pw_hash))

        row = cur.fetchone()
        cur.close(); conn.close()

        if not row:
            return jsonify({"status":"error","message":"Usuario o contraseña incorrectos"}), 401

        return jsonify({
            "status":"success",
            "user":{
                "id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "role": row[4]
            }
        }), 200

    except Exception as e:
        print("❌ login_user:", type(e).__name__, str(e))
        if 'conn' in locals() and not conn.closed:
            cur.close(); conn.close()
        return jsonify({"status":"error","message":"Error en el servidor"}), 500
