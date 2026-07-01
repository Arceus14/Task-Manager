from bson.objectid import ObjectId

from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.task import Task
from utils.validators import validate_task_create, validate_task_update

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    """
    Create Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    data = request.get_json(silent=True) or {}

    error = validate_task_create(data)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), 400

    description = data.get("description", "")

    task = Task.create(
        data["title"].strip(),
        description.strip() if isinstance(description, str) else "",
        get_jwt_identity()
    )

    return jsonify({
        "success": True,
        "data": task
    }), 201


@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    """
    Get My Tasks (all tasks if admin)
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    role = get_jwt().get("role")

    if role == "admin":
        tasks = Task.get_all()
    else:
        tasks = Task.get_all(get_jwt_identity())

    return jsonify({
        "success": True,
        "data": tasks
    })


@task_bp.route("/<task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    """
    Get Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    task = Task.get(task_id)

    if not task:
        return jsonify({
            "success": False,
            "message": "Task not found."
        }), 404

    is_owner = task["owner"] == get_jwt_identity()
    is_admin = get_jwt().get("role") == "admin"

    if not is_owner and not is_admin:
        return jsonify({
            "success": False,
            "message": "Forbidden."
        }), 403

    task["_id"] = str(task["_id"])

    return jsonify({
        "success": True,
        "data": task
    })


@task_bp.route("/<task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    """
    Update Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    task = Task.get(task_id)

    if not task:
        return jsonify({
            "success": False,
            "message": "Task not found."
        }), 404

    is_owner = task["owner"] == get_jwt_identity()
    is_admin = get_jwt().get("role") == "admin"

    if not is_owner and not is_admin:
        return jsonify({
            "success": False,
            "message": "Forbidden."
        }), 403

    data = request.get_json(silent=True) or {}

    error = validate_task_update(data)

    if error:
        return jsonify({
            "success": False,
            "message": error
        }), 400

    update_data = {}

    if "title" in data:
        update_data["title"] = data["title"].strip()

    if "description" in data:
        update_data["description"] = data["description"].strip()

    if "completed" in data:
        update_data["completed"] = data["completed"]

    Task.update(task_id, update_data)

    return jsonify({
        "success": True,
        "message": "Task updated."
    })


@task_bp.route("/<task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    """
    Delete Task
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    """

    task = Task.get(task_id)

    if not task:
        return jsonify({
            "success": False,
            "message": "Task not found."
        }), 404

    is_owner = task["owner"] == get_jwt_identity()
    is_admin = get_jwt().get("role") == "admin"

    if not is_owner and not is_admin:
        return jsonify({
            "success": False,
            "message": "Forbidden."
        }), 403

    Task.delete(task_id)

    return jsonify({
        "success": True,
        "message": "Task deleted."
    })