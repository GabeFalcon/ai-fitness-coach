from flask import Blueprint, request
from datetime import datetime
from database.db import get_connection
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

    conn = get_connection()
    cursor = conn.cursor()

    # 1. GET CURRENT DAY COUNT
    cursor.execute(
        "SELECT COUNT(*) as count FROM checkins WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    day_number = (row["count"] + 1) if row else 1

    # 2. STORE CHECKIN (convert dict → JSON string)
    cursor.execute("""
        INSERT INTO checkins (user_id, day, date, exercises)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        day_number,
        datetime.now().isoformat(),
        json.dumps(exercises)
    ))

    conn.commit()
    conn.close()

    # 3. STILL UPDATE ANALYTICS (keeps your AI features alive)
    update_exercise_history(user_id, exercises)

    return {
        "message": "check-in saved",
        "day": day_number,
        "total_checkins": day_number
    }