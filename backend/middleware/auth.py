from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify


def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):

        claims = get_jwt()

        if claims["role"] != "admin":

            return jsonify({
                "success": False,
                "message": "Admins only."
            }), 403

        return fn(*args, **kwargs)

    return wrapper