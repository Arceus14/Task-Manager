from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flasgger import Swagger


mongo = PyMongo()

jwt = JWTManager()

swagger = Swagger()