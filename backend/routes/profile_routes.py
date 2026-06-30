from flask import Blueprint, request
from database.db import get_connection

profile_bp = Blueprint("profile", __name__)

ALLOWED_GOALS = [
    "fat_loss",
    "muscle_gain",
    "maintenance",
    "fat_loss_and_muscle_gain"
]

ALLOWED_EXPERIENCE = [
    "beginner",
    "intermediate",
    "advanced"
]


# -----------------------
# STORE USER PROFILE
# -----------------------

@profile_bp.route("/onboarding", methods=["POST"])
def onboarding():
    data = request.get_json()

    if not data:
        return {"error": "no JSON provided"}, 400

    required = [
        "user_id",
        "age",
        "weight",
        "height",
        "days_per_week",
        "goal",
        "experience"
    ]

    for field in required:
        if field not in data:
            return {"error": f"missing field: {field}"}, 400

    if data["goal"] not in ALLOWED_GOALS:
        return {"error": "invalid goal"}, 400

    if data["experience"] not in ALLOWED_EXPERIENCE:
        return {"error": "invalid experience"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    # Make sure user exists
    cursor.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (data["user_id"],)
    )

    if cursor.fetchone() is None:
        conn.close()
        return {"error": "user not found"}, 404

    # Save profile
    cursor.execute("""
        INSERT OR REPLACE INTO profiles
        (
            user_id,
            age,
            weight,
            height,
            days_per_week,
            goal,
            experience
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["user_id"],
        int(data["age"]),
        float(data["weight"]),
        int(data["height"]),
        int(data["days_per_week"]),
        data["goal"],
        data["experience"]
    ))

    conn.commit()
    conn.close()

    return {"message": "profile created"}


# -----------------------
# GET PROFILE
# -----------------------

@profile_bp.route("/profile", methods=["GET"])
def profile():

    user_id = request.args.get("user_id")

    if not user_id:
        return {"error": "missing user_id"}, 400

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM profiles WHERE user_id = ?",
        (user_id,)
    )

    profile = cursor.fetchone()

    conn.close()

    if profile is None:
        return {"error": "profile not found"}, 404

    return dict(profile)