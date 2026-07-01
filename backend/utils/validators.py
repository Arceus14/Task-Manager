import re


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


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