from flask import Blueprint, request, jsonify, make_response
from core_auth import create_jwt, cookie_opts, current_user
from db import get_db_connection
import bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/login")
def login():
    data     = request.get_json(silent=True) or {}
    email    = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Credenciales inválidas"}), 400

    conn = get_db_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT id, first_name, last_name, email,
               COALESCE(password_hash,''), COALESCE(is_admin, false)
        FROM oogsj_data."user"
        WHERE LOWER(email) = LOWER(%s)
    """, (email,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row or not row[4] or not bcrypt.checkpw(password.encode(), row[4].encode()):
        return jsonify({"error": "Email o contraseña incorrectos"}), 401

    token = create_jwt({
        "uid":        row[0],
        "email":      row[3],
        "first_name": row[1],
        "last_name":  row[2],
        "is_admin":   row[5],
    })
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("auth_token", token, **cookie_opts())
    return resp


@auth_bp.post("/logout")
def logout():
    resp = make_response(jsonify({"ok": True}))
    resp.set_cookie("auth_token", "", expires=0, **cookie_opts())
    return resp


@auth_bp.get("/me")
def me():
    u = current_user()
    if not u:
        return jsonify({"authenticated": False}), 200
    return jsonify({"authenticated": True, "user": u}), 200