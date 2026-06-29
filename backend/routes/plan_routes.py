from flask import Blueprint, request
from datetime import datetime
from database.memory_db import db
from utils.validators import validate_user_request
from services.ai_service import generate_ai_plan

plan_bp = Blueprint("plan", __name__)

# GENERATE PLAN
@plan_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json()

    user_id, error = validate_user_request(data)
    if error:
        return error, 400

    profile = db["profiles"][user_id]

    # Store the plan
    plan = generate_ai_plan(profile)

    db["plans"][user_id] = {
    "content": plan,
    "version": 1,
    "created_at": datetime.now().isoformat()
    }

    return {
        "user_id": user_id,
        "plan": plan
    }


# PLAN RETRIEVAL
@plan_bp.route("/plan", methods=["GET"])
def get_plan():
    user_id = request.args.get("user_id")

    if not user_id:
        return {"error": "missing user_id"}, 400

    if user_id not in db["profiles"]:
        return {"error": "profile not found"}, 404

    return db["plans"].get(user_id, {"error": "no plan found"})