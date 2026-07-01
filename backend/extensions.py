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
        }
    }
)