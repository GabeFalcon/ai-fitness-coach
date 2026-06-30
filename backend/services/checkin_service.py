from database.db import get_connection
from datetime import datetime
import json


def update_exercise_history(user_id, exercises):
    """
    Converts raw check-in exercises into structured progress logs.
    """

    conn = get_connection()
    cursor = conn.cursor()

    for exercise_name, exercise_data in exercises.items():
        sets = exercise_data.get("sets", [])

        if not sets:
            continue

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

        cursor.execute("""
            INSERT INTO exercise_history (
                user_id,
                exercise_name,
                avg_reps,
                avg_weight,
                sets_completed,
                date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            exercise_name,
            avg_reps,
            avg_weight,
            valid_sets,
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()

    return True