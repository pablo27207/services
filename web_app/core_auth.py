from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, jsonify
from passlib.hash import bcrypt

from config import JWT_SECRET, JWT_ISS, JWT_EXP_MIN, SECURE_COOKIES


def create_jwt(payload: dict) -> str:
    now = datetime.utcnow()
    to_encode = {
        "iss": JWT_ISS,
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXP_MIN),
        **payload,
    }
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")


def decode_jwt(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer=JWT_ISS)


def cookie_opts() -> dict:
    return dict(httponly=True, secure=SECURE_COOKIES, samesite="Lax", path="/")


def current_user():
    tok = request.cookies.get("auth_token")
    if not tok:
        return None
    try:
        data = decode_jwt(tok)
        return {
            "id":         data.get("uid"),
            "email":      data.get("email"),
            "first_name": data.get("first_name"),
            "last_name":  data.get("last_name"),
            "is_admin":   bool(data.get("is_admin")),
        }
    except Exception:
        return None


def admin_required(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        u = current_user()
        if not u or not u["is_admin"]:
            return jsonify({"error": "No autorizado"}), 401
        return fn(*args, **kwargs)
    return _wrap