from flask import Blueprint, request, jsonify
from core_auth import master_required, current_user
from db import get_db_connection
import bcrypt
import re

users_bp = Blueprint("users", __name__, url_prefix="/api/admin/users")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@users_bp.get("/")
@master_required
def list_users():
    """Lista todos los usuarios admin registrados."""
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT id, first_name, last_name, email, is_admin, admin_role, created_at
            FROM oogsj_data."user"
            WHERE is_admin = true
            ORDER BY created_at ASC;
        """)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    users = [
        {
            "id":         r[0],
            "first_name": r[1],
            "last_name":  r[2],
            "email":      r[3],
            "is_admin":   r[4],
            "admin_role": r[5],
            "created_at": r[6].isoformat() if r[6] else None,
        }
        for r in rows
    ]
    return jsonify({"users": users})


@users_bp.post("/")
@master_required
def create_user():
    """Crea un nuevo usuario admin (master o viewer)."""
    body       = request.get_json(silent=True) or {}
    first_name = (body.get("first_name") or "").strip()
    last_name  = (body.get("last_name")  or "").strip()
    email      = (body.get("email")      or "").strip().lower()
    password   = body.get("password")   or ""
    admin_role = (body.get("admin_role") or "viewer").strip()

    if not first_name or not last_name:
        return jsonify({"error": "Nombre y apellido son obligatorios"}), 400
    if not email or not _EMAIL_RE.match(email):
        return jsonify({"error": "Email inválido"}), 400
    if len(password) < 8:
        return jsonify({"error": "La contraseña debe tener al menos 8 caracteres"}), 400
    if admin_role not in ("master", "viewer"):
        return jsonify({"error": "Rol inválido. Debe ser 'master' o 'viewer'"}), 400

    me = current_user()
    if admin_role == "master" and me.get("admin_role") != "master":
        return jsonify({"error": "Solo un master puede crear otro master"}), 403

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            SELECT id FROM oogsj_data."user" WHERE LOWER(email) = %s;
        """, (email,))
        if cur.fetchone():
            return jsonify({"error": "Ya existe un usuario con ese email"}), 409

        cur.execute("""
            INSERT INTO oogsj_data."user"
                (first_name, last_name, email, password_hash, is_admin, admin_role)
            VALUES (%s, %s, %s, %s, true, %s)
            RETURNING id, first_name, last_name, email, admin_role, created_at;
        """, (first_name, last_name, email, pw_hash, admin_role))
        row = cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Error al crear el usuario", "detail": str(e)}), 500
    finally:
        cur.close()
        conn.close()

    return jsonify({
        "user": {
            "id":         row[0],
            "first_name": row[1],
            "last_name":  row[2],
            "email":      row[3],
            "admin_role": row[4],
            "created_at": row[5].isoformat() if row[5] else None,
        }
    }), 201


@users_bp.delete("/<int:user_id>")
@master_required
def delete_user(user_id):
    """Elimina un usuario admin. Un master no puede eliminarse a sí mismo."""
    me = current_user()
    if me["id"] == user_id:
        return jsonify({"error": "No podés eliminar tu propia cuenta"}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("""
            DELETE FROM oogsj_data."user"
            WHERE id = %s AND is_admin = true
            RETURNING id;
        """, (user_id,))
        row = cur.fetchone()
        conn.commit()
    finally:
        cur.close()
        conn.close()

    if not row:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"ok": True})
