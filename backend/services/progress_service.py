from database.memory_db import db


# Analyze user exercise history and return progress insights.
def analyze_progress(user_id):

    history = db["exercise_history"].get(user_id, {})

    if not history:
        return {
            "status": "no_data",
            "insights": []
        }

    insights = []

    for exercise_name, sessions in history.items():

        if len(sessions) < 2:
            continue

        latest = sessions[-1]
        previous = sessions[-2]

        # safe extraction (prevents crashes)
        latest_reps = latest.get("avg_reps", 0)
        previous_reps = previous.get("avg_reps", 0)

        latest_weight = latest.get("avg_weight", 0)
        previous_weight = previous.get("avg_weight", 0)

        rep_change = latest_reps - previous_reps
        weight_change = latest_weight - previous_weight

        # default
        trend = "stable"
        message = "No major change detected"

        # logic
        if rep_change > 0 and weight_change >= 0:
            trend = "improving"
            message = "Strength is increasing"

        elif rep_change < 0 and weight_change <= 0:
            trend = "declining"
            message = "Possible fatigue or recovery issue"

        else:
            trend = "mixed"
            message = "Some progression inconsistency"

        insights.append({
            "exercise": exercise_name,
            "trend": trend,
            "rep_change": round(rep_change, 2),
            "weight_change": round(weight_change, 2),
            "message": message
        })

    return {
        "status": "analyzed",
        "insights": insights
    }