from flask import Blueprint

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/health")
def task_health():
    return {
        "message": "Task routes working."
    }