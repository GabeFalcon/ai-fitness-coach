from database.memory_db import db

def get_user_context(user_id):
    profile = db["profiles"].get(user_id)
    plan = db["plans"].get(user_id)
    checkins = db["checkins"].get(user_id, [])
    history = db["exercise_history"].get(user_id, {})

    if not profile:
        return None

    return {
        "profile": profile,
        "plan": plan,
        "checkins": checkins,
        "exercise_history": history
    }