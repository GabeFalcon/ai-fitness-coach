from database.db import get_connection


def analyze_progress(user_id):
    """
    Analyzes last 7 sessions per exercise and detects trends.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT exercise_name, avg_reps, avg_weight, date
        FROM exercise_history
        WHERE user_id = ?
        ORDER BY date ASC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {
            "status": "no_data",
            "insights": []
        }

    history = {}

    # group by exercise
    for r in rows:
        ex = r["exercise_name"]

        if ex not in history:
            history[ex] = []

        history[ex].append({
            "avg_reps": r["avg_reps"],
            "avg_weight": r["avg_weight"],
            "date": r["date"]
        })

    insights = []

    for exercise_name, sessions in history.items():

        if len(sessions) < 7:
            continue

        latest = sessions[-1]
        previous = sessions[-7]

        rep_change = latest["avg_reps"] - previous["avg_reps"]
        weight_change = latest["avg_weight"] - previous["avg_weight"]

        trend = "stable"
        message = "No major change detected"

        if rep_change > 0 and weight_change > 0:
            trend = "improving"
            message = "Strength is increasing"

        elif rep_change < 0 and weight_change < 0:
            trend = "declining"
            message = "Possible fatigue or recovery issue"

        else:
            trend = "mixed"
            message = "Inconsistent progression"

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