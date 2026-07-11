from database.memory_db import db

def get_user_context(user_id):
    profile = db["profiles"].get(user_id)
    plan = db["plans"].get(user_id) or {}
    checkins = db["checkins"].get(user_id, []) or []
    history = db["exercise_history"].get(user_id, {}) or {}

    if not profile:
        return None

    # ensure plan always exists
    if not plan:
        plan = {}

    return {
        "profile": profile,
        "plan": plan,
        "checkins": checkins,
        "exercise_history": history
    }