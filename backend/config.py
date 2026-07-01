import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SWAGGER = {
        "title": "Task Manager API",
        "uiversion": 3
    }