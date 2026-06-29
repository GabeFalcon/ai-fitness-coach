from flask import Blueprint, request
from database.memory_db import db

profile_bp = Blueprint("profile", __name__)

# CONSTANTS
ALLOWED_GOALS = ["fat_loss", "muscle_gain", "maintenance", "fat_loss_and_muscle_gain"]

ALLOWED_EXPERIENCE = ["beginner", "intermediate", "advanced"]

# STORE USER DATA
@profile_bp.route("/onboarding", methods=["POST"])
def onboarding():
    data = request.get_json()

    # Ensure data exists
    if not data:
        return {"error": "no JSON provided"}, 400

    required = ["age", "weight", "height", "days_per_week",
                 "goal", "experience", "user_id"]
    
    for f in required:
        if f not in data:
            return {"error": f"missing field: {f}"}, 400

    if data["goal"] not in ALLOWED_GOALS:
        return {"error": "invalid goal"}, 400
    
    if data["experience"] not in ALLOWED_EXPERIENCE:
        return {"error": "invalid experience"}, 400
    
    if data["user_id"] not in db["users"]:
        return {"error": "user not found"}, 404

    # Store the data
    db["profiles"][data["user_id"]] = {
        "age": int(data["age"]),
        "weight": float(data["weight"]),
        "height": int(data["height"]),
        "days_per_week": int(data["days_per_week"]),
        "goal": data["goal"],
        "experience": data["experience"]
    }

    return {"message": "profile created"}

# RETRIEVE USER DATA
@profile_bp.route("/profile", methods=["GET"])
def profile():
    user_id = request.args.get("user_id")

    if not user_id:
        return {"error": "missing user_id"}, 400

    if user_id not in db["profiles"]:
        return {"error": "profile not found"}, 404

    return {
        "user_id": user_id,
        "data": db["profiles"][user_id]
    }