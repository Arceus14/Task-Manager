from flask import Blueprint

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/health")
def auth_health():
    return {
        "message": "Authentication routes working."
    }