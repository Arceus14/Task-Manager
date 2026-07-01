import re


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"

TITLE_MAX_LENGTH = 200
DESCRIPTION_MAX_LENGTH = 2000


def validate_register(data):

    if "name" not in data:
        return "Name is required"

    if "email" not in data:
        return "Email is required"

    if "password" not in data:
        return "Password is required"

    if not re.match(EMAIL_REGEX, data["email"]):
        return "Invalid email"

    if len(data["password"]) < 6:
        return "Password must be at least 6 characters"

    return None


def validate_task_create(data):

    if not isinstance(data, dict):
        return "Request body must be a JSON object."

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return "Title is required and must be a non-empty string."

    if len(title.strip()) > TITLE_MAX_LENGTH:
        return f"Title must be at most {TITLE_MAX_LENGTH} characters."

    description = data.get("description", "")

    if description is not None and not isinstance(description, str):
        return "Description must be a string."

    if isinstance(description, str) and len(description) > DESCRIPTION_MAX_LENGTH:
        return f"Description must be at most {DESCRIPTION_MAX_LENGTH} characters."

    return None


def validate_task_update(data):

    if not isinstance(data, dict) or not data:
        return "Request body must include at least one field to update."

    allowed_fields = {"title", "description", "completed"}

    if not any(field in data for field in allowed_fields):
        return "Provide at least one of: title, description, completed."

    if "title" in data:

        if not isinstance(data["title"], str) or not data["title"].strip():
            return "Title must be a non-empty string."

        if len(data["title"].strip()) > TITLE_MAX_LENGTH:
            return f"Title must be at most {TITLE_MAX_LENGTH} characters."

    if "description" in data:

        if not isinstance(data["description"], str):
            return "Description must be a string."

        if len(data["description"]) > DESCRIPTION_MAX_LENGTH:
            return f"Description must be at most {DESCRIPTION_MAX_LENGTH} characters."

    if "completed" in data:

        if not isinstance(data["completed"], bool):
            return "Completed must be true or false."

    return None