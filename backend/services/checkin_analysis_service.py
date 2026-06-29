def analyze_checkins(checkins):
    """
    Analyze progression across recent workouts
    """

    if not checkins or len(checkins) < 3:
        return {
            "trend": "insufficient_data",
            "insights": []
        }

    insights = []

    latest = checkins[-1]
    latest_exercises = latest["exercises"]

    # look back across multiple sessions
    history = checkins[-6:-1]  # last 5 sessions before latest

    for exercise_name, latest_data in latest_exercises.items():

        latest_sets = latest_data["sets"]
        latest_avg_reps = sum(s["reps"] for s in latest_sets) / len(latest_sets)

        past_avgs = []

        # collect past performance for same exercise
        for past in history:
            past_ex = past["exercises"]

            if exercise_name not in past_ex:
                continue

            past_sets = past_ex[exercise_name]["sets"]
            avg = sum(s["reps"] for s in past_sets) / len(past_sets)
            past_avgs.append(avg)

        if not past_avgs:
            continue

        avg_past = sum(past_avgs) / len(past_avgs)

        # compare trend
        diff = latest_avg_reps - avg_past

        if diff > 1:
            insights.append({
                "exercise": exercise_name,
                "trend": "improving",
                "message": "Strength or endurance is increasing",
                "delta": round(diff, 2)
            })

        elif diff < -1:
            insights.append({
                "exercise": exercise_name,
                "trend": "declining",
                "message": "Possible fatigue or overload",
                "delta": round(diff, 2)
            })

        else:
            insights.append({
                "exercise": exercise_name,
                "trend": "stable",
                "message": "Performance is consistent",
                "delta": round(diff, 2)
            })

    return {
        "trend": "analyzed",
        "insights": insights
    }