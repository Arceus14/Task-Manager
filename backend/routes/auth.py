from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from utils.validators import validate_register

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Syed
            email:
              type: string
              example: syed@test.com
            password:
              type: string
              example: password123
    responses:
      201:
        description: User created successfully
      400:
        description: Validation error
      409:
        description: Email already exists
    """
    data = request.get_json(silent=True) or {}
    error = validate_register(data)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), 400

    existing = User.find_by_email(data["email"])
    if existing:
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    role = "user"
    user = User.create(
        data["name"],
        data["email"],
        data["password"],
        role
    )

    return jsonify({
        "success": True,
        "message": "User created.",
        "data": user
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: syed@test.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    user = User.find_by_email(email)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid credentials."
        }), 401

    if not User.verify_password(
        password,
        user["password"]
    ):
        return jsonify({
            "success": False,
            "message": "Invalid credentials."
        }), 401

    token = create_access_token(
        identity=str(user["_id"]),
        additional_claims={
            "role": user["role"]
        }
    )

    return jsonify({
        "success": True,
        "token": token,
        "role": user["role"]
    })
