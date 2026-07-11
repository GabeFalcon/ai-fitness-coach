from flask import Blueprint, request
from utils.validators import validate_user_request
from utils.user_context import get_user_context
from services.progress_service import analyze_progress
from services.ai_service import coach_chat
from services.plan_service import apply_ai_adjustment
from database.db import get_connection

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_id, error = validate_user_request(data)
    if error:
        return error, 400

    user_message = data.get("message")
    if not user_message:
        return {"error": "missing message"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    # ✅ SINGLE SOURCE OF TRUTH CHECK
    cursor.execute(
        "SELECT * FROM profiles WHERE user_id = ?",
        (user_id,)
    )

    profile_row = cursor.fetchone()
    print("PROFILE ROW:", profile_row)

    if not profile_row:
        conn.close()
        return {"error": f"profile not found for {user_id}"}, 404

    # ✅ build context manually (DO NOT rely on broken helper yet)
    context = {
        "profile": dict(profile_row)
    }

    progress = analyze_progress(user_id)

    response = coach_chat(
        context=context,
        user_message=user_message,
        progress=progress
    )

    updated_plan = apply_ai_adjustment(user_id, response)

    conn.close()

    return {
        "user_id": user_id,
        "response": response,
        "updated_plan": updated_plan
    }