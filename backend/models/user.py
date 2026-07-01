from datetime import datetime
from bson.objectid import ObjectId
from extensions import mongo
import bcrypt


class User:

    @staticmethod
    def create(name, email, password, role="user"):

        hashed = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        user = {
            "name": name,
            "email": email.lower(),
            "password": hashed.decode("utf-8"),
            "role": role,
            "created_at": datetime.utcnow()
        }

        result = mongo.db.users.insert_one(user)

        user["_id"] = str(result.inserted_id)

        del user["password"]

        return user

    @staticmethod
    def find_by_email(email):

        return mongo.db.users.find_one({
            "email": email.lower()
        })

    @staticmethod
    def find_by_id(user_id):

        return mongo.db.users.find_one({
            "_id": ObjectId(user_id)
        })

    @staticmethod
    def verify_password(password, hashed):

        return bcrypt.checkpw(
            password.encode(),
            hashed.encode()
        )