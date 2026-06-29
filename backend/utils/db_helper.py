from database.memory_db import db

def ensure_user_collections(user_id):
    if user_id not in db["checkins"]:
        db["checkins"][user_id] = []

    if user_id not in db["exercise_history"]:
        db["exercise_history"][user_id] = {}

    if user_id not in db["messages"]:
        db["messages"][user_id] = []