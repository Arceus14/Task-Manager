from datetime import datetime
from bson.objectid import ObjectId
from extensions import mongo


class Task:
    @staticmethod
    def create(title, description, owner_id):

        task = {
            "title": title,
            "description": description,
            "completed": False,
            "owner": owner_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        result = mongo.db.tasks.insert_one(task)

        task["_id"] = str(result.inserted_id)

        return task
    
    @staticmethod
    def get_all(owner_id=None):

        query = {}

        if owner_id:
            query["owner"] = owner_id
        
        tasks = []

        for task in mongo.db.tasks.find(query):

            task["_id"] = str(task["_id"])

            tasks.append(task)

        return tasks
    
    @staticmethod
    def get(task_id):

        return mongo.db.tasks.find_one({
            "_id": ObjectId(task_id)
        })
    
    @staticmethod
    def update(task_id, data):

        data["updated_at"] = datetime.now()

        mongo.db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": data}
        )
    
    @staticmethod
    def delete(task_id):

        mongo.db.tasks.delete_one({
            "_id": ObjectId(task_id)
        })