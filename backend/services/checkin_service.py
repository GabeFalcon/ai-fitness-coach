from database.memory_db import db
from datetime import datetime


def update_exercise_history(user_id, exercises):

    if user_id not in db["exercise_history"]:
        db["exercise_history"][user_id] = {}

    user_history = db["exercise_history"][user_id]

    for exercise_name, exercise_data in exercises.items():
        sets = exercise_data.get("sets", [])

        if not sets:
            continue  # skip invalid entry

        total_reps = 0
        total_weight = 0

        valid_sets = 0

        for s in sets:
            reps = s.get("reps")
            weight = s.get("weight")

            if reps is None or weight is None:
                continue

            total_reps += reps
            total_weight += weight
            valid_sets += 1

        if valid_sets == 0:
            continue

        avg_reps = total_reps / valid_sets
        avg_weight = total_weight / valid_sets

        if exercise_name not in user_history:
            user_history[exercise_name] = []

        user_history[exercise_name].append({
            "date": datetime.now().isoformat(),
            "avg_reps": avg_reps,
            "avg_weight": avg_weight,
            "sets_completed": valid_sets
        })

    return user_history