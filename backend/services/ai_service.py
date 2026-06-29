from openai import OpenAI

client = OpenAI()


#-----------------
# PROMPTS
#-----------------
def build_prompt(profile):
    return f"""
    You are an elite fitness coach AI. Your ultimate goal is to help the user reach their goal phsyique. 

    Create a personalized training and nutrition plan.

    User Profile:
    - Age: {profile['age']}
    - Weight: {profile['weight']}
    - Height: {profile['height']}
    - Goal: {profile['goal']}
    - Experience: {profile['experience']}
    - Training days per week: {profile['days_per_week']}

    Rules:
    - Be realistic and safe
    - Keep it structured and easy to follow
    - Do NOT be generic
    - Adapt intensity to experience level
    - Include workout, diet, and reasoning

    Return format:

    {{
        "plan_type": "...",

        "workouts": {{
            "push_day": [
                {{
                    "exercise": "Bench Press",
                    "sets": [
                        {{"reps": 10, "weight": 135}},
                        {{"reps": 8, "weight": 135}},
                        {{"reps": 6, "weight": 135}}
                    ]
                }}
            ]
        }},
        
        "diet": {{
        "calories": 2200,
        "protein": 180,
        "carbs": 220,
        "fat": 65
        }}
    }}
    """

# Plan Adjuster / Recommender
def build_adjustment_prompt(profile, plan, checkins, user_message, progress):
    return f"""
    You are an adaptive fitness coach AI that manages a living training plan.

    You are NOT allowed to randomly rewrite the plan.

    You must decide ONE of the following:

    1. KEEP PLAN (no changes needed)
    2. SMALL ADJUSTMENT (minor edits like reps, volume, cardio)
    3. MAJOR ADJUSTMENT (only if progress is clearly stalled or user requests it)

    USER MESSAGE:
    {user_message}

    CURRENT PLAN:
    {plan}

    CHECK-IN HISTORY:
    {checkins}

    USER PROFILE:
    - Age: {profile['age']}
    - Weight: {profile['weight']}
    - Goal: {profile['goal']}
    - Experience: {profile['experience']}
    - Training days: {profile['days_per_week']}
    - Progress Analysis: {progress}
    
    RULES:
    - Decide if plan should change
    - Be conservative with changes
    - Do NOT change everything unless necessary
    - Explain WHY you changed or did NOT change

    OUTPUT JSON:
    decision (keep|small_adjustment|major_adjustment)
    plan_type
    workout
    diet
    notes
"""

# ----------------------
# AI FUNCTIONS
# ----------------------

def generate_ai_plan(profile):

    prompt = build_prompt(profile)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are CoachAI, an elite fitness coach."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def coach_chat(context, user_message):

    prompt = build_adjustment_prompt(
        context["profile"],
        context["plan"],
        context["checkins"],
        user_message
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are CoachAI, an adaptive fitness coach."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content