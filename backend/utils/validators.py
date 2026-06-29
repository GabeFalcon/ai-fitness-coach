from database.memory_db import db

def validate_user_request(data):
    if not data:
        return None, {"error": "no JSON provided"}

    user_id = data.get("user_id")
    if not user_id:
        return None, {"error": "missing user_id"}

    if user_id not in db["users"]:
        return None, {"error": "user does not exist"}

    return user_id, None