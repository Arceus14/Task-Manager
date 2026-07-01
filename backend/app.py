from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from bson.errors import InvalidId

from config import Config
from extensions import mongo, jwt, swagger

from routes.auth import auth_bp
from routes.tasks import task_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)
    mongo.init_app(app)
    jwt.init_app(app)
    swagger.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(task_bp, url_prefix="/api/v1/tasks")

    @app.route("/")
    def home():
        return {
            "message": "Task Manager  API is running successfully."
        }

    @app.route("/api/v1/health")
    def health():
        return jsonify({
            "success": True,
            "status": "healthy",
            "version": "1.0.0"
        })

    register_error_handlers(app)
    register_jwt_handlers()

    return app


def register_error_handlers(app):

    # Someone passed a task id that isn't a valid Mongo ObjectId
    # (e.g. GET /api/v1/tasks/abc123) -> clean 400 instead of a raw 500.
    @app.errorhandler(InvalidId)
    def handle_invalid_id(err):
        return jsonify({
            "success": False,
            "message": "Invalid id format."
        }), 400

    # Anything Flask/Werkzeug raises with a real status code
    # (404 unknown route, 405 wrong method, 401/403 if ever raised
    # via abort(), etc.) -> same JSON shape, real status code kept.
    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return jsonify({
            "success": False,
            "message": err.description or err.name
        }), err.code

    # Anything else unexpected -> 500, logged server-side,
    # generic message client-side (no stack trace leakage).
    @app.errorhandler(Exception)
    def handle_unexpected_error(err):
        app.logger.exception(err)
        return jsonify({
            "success": False,
            "message": "Something went wrong. Please try again."
        }), 500


def register_jwt_handlers():

    # Request had no Authorization header at all
    @jwt.unauthorized_loader
    def missing_token_callback(err):
        return jsonify({
            "success": False,
            "message": "Authorization token is required."
        }), 401

    # Token present but malformed / signature invalid
    @jwt.invalid_token_loader
    def invalid_token_callback(err):
        return jsonify({
            "success": False,
            "message": "Invalid or malformed token."
        }), 401

    # Token present but expired
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "message": "Token has expired. Please log in again."
        }), 401


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)