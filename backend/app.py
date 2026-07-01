from flask import Flask
from config import Config
from extensions import mongo, jwt, swagger

from routes.auth import auth_bp
from routes.tasks import task_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

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
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)