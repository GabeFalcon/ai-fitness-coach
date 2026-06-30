from flask import Blueprint, request
from datetime import datetime
from database.db import get_connection
from utils.validators import validate_user_request
from services.ai_service import generate_ai_plan
import json

plan_bp = Blueprint("plan", __name__)

# GENERATE PLAN
@plan_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json()

    user_id, error = validate_user_request(data)
    if error:
        return error, 400

    conn = get_connection()
    cursor = conn.cursor()

    # 1. GET PROFILE FROM DB
    cursor.execute(
        "SELECT * FROM profiles WHERE user_id = ?",
        (user_id,)
    )
    profile = cursor.fetchone()

    if not profile:
        conn.close()
        return {"error": "profile not found"}, 404

    profile = dict(profile)

    # 2. GENERATE AI PLAN
    plan = generate_ai_plan(profile)
    plan_json = json.dumps(plan)

    # 3. UPSERT PLAN (insert or replace)
    cursor.execute("""
        INSERT INTO plans (user_id, content, version, created_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            content = excluded.content,
            version = plans.version + 1,
            created_at = excluded.created_at
    """, (
        user_id,
        plan_json,
        1,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()

    return {
        "user_id": user_id,
        "plan": json.loads(plan_json)
    }



# PLAN RETRIEVAL
@plan_bp.route("/plan", methods=["GET"])
def get_plan():
    user_id = request.args.get("user_id")

    if not user_id:
        return {"error": "missing user_id"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM plans WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    conn.close()

    if not row:
        return {"error": "no plan found"}, 404

    data = dict(row)
    data["content"] = json.loads(data["content"])
    return data