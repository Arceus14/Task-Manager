from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flasgger import Swagger


mongo = PyMongo()

jwt = JWTManager()

swagger = Swagger(
    template={
        "swagger": "2.0",
        "info": {
            "title": "Task Manager API",
            "description": "Backend API for Primetrade.ai Internship Assignment",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Paste **Bearer &lt;your JWT&gt;** (include the word Bearer). Get a token from POST /api/v1/auth/login."
            }
        }
    }
)