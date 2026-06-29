from flask import Blueprint, request
import uuid
from database.memory_db import db

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

    # Make sure the email is unique
    for existing_user in db["users"].values():
        if existing_user.get("email") == data["email"]:
            return {"error": "account with email exsits"}, 400
    
    user_id = str(uuid.uuid4())

    # Store the user data
    db["users"][user_id] = {
        "user_id": user_id,
        "email": data["email"],
        "username": data["username"],
        "password": data["password"]
    }

    return {"user_id": user_id}
