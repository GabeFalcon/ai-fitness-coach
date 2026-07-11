import copy

def merge_plan_changes(current_plan, workout_changes):
    updated_plan = copy.deepcopy(current_plan)

    workouts = updated_plan.get("workouts", {})

    for day, exercises in workouts.items():
        for exercise in exercises:
            name = exercise.get("exercise")

            if name in workout_changes:
                change = workout_changes[name]
                if "sets" in change:
                    exercise["sets"] = change["sets"]

    return updated_plan