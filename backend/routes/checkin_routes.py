from flask import Blueprint, request
from datetime import datetime
from database.memory_db import db
from utils.validators import validate_user_request
from services.checkin_service import update_exercise_history

checkin_bp = Blueprint("checkin", __name__)

# DAILY CHECKIN SYSTEM
@checkin_bp.route("/checkin", methods=["POST"])
def checkin():
    data = request.get_json()

    user_id, error = validate_user_request(data)
    if error:
        return error, 400

    exercises = data.get("exercises")
    if not exercises:
        return {"error": "missing exercises"}, 400

    if user_id not in db["checkins"]:
        db["checkins"][user_id] = []

    checkin_entry = {
        "day": len(db["checkins"][user_id]) + 1,
        "date": datetime.now().isoformat(),
        "exercises": exercises
    }

    db["checkins"][user_id].append(checkin_entry)
    update_exercise_history(user_id, exercises)

    return {
        "message": "check-in saved",
        "checkin": checkin_entry,
        "total_checkins": len(db["checkins"][user_id])
    }
