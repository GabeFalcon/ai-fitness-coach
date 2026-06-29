from flask import Blueprint, request
from database.memory_db import db
from utils.validators import validate_user_request
from utils.user_context import get_user_context
from services.progress_service import analyze_progress
from services.ai_service import coach_chat

chat_bp = Blueprint("chat", __name__)

# AI Coach Chat
@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    user_id, error = validate_user_request(data)
    if error:
        return error, 400
    
    user_message = data.get("message")
    if not user_message:
        return {"error": "missing message"}, 400
    
    context = get_user_context(user_id)
    if not context:
        return {"error": "profile not found"}, 404
    
    progress = analyze_progress(user_id)
    
    response = coach_chat(
        profile=context["profile"],
        plan=context["plan"],
        checkins=context["checkins"],
        user_message=user_message,
        progress = progress
    )

    return {
        "user_id": user_id,
        "response": response
    }