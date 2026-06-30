from flask import Blueprint, request
import uuid
from database.db import get_connection

auth_bp = Blueprint("auth", __name__)

# ACCOUNT CREATION
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data:
        return {"error": "no JSON provided"}, 400

    required = ["email", "username", "password"]
    # Make sure each field(r) has been submitted
    for f in required:
        if f not in data:
            return {"error": f"missing field: {f}"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    # 1. CHECK IF EMAIL EXISTS
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (data["email"],)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return {"error": "account with email exists"}, 400

    # 2. CREATE USER
    user_id = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO users (user_id, email, username, password)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        data["email"],
        data["username"],
        data["password"]
    ))

    conn.commit()
    conn.close()

    return {"user_id": user_id}
