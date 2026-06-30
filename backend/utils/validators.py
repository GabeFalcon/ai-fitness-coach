from database.db import get_connection

def validate_user_request(data):
    if not data:
        return None, {"error": "no JSON provided"}

    user_id = data.get("user_id")
    if not user_id:
        return None, {"error": "missing user_id"}

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    if not user:
        return None, {"error": "user does not exist"}

    return user_id, None