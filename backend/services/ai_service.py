from openai import OpenAI
import json
from services.ai_safety_parser import safe_parse_ai_response
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing from environment")

client = OpenAI(api_key=api_key)

# -------------------------
# PROMPT: INITIAL PLAN
# -------------------------
def build_prompt(profile):
    return f"""
You are an elite fitness coach AI.

Create a personalized training and nutrition plan.

User Profile:
- Age: {profile['age']}
- Weight: {profile['weight']}
- Height: {profile['height']}
- Goal: {profile['goal']}
- Experience: {profile['experience']}
- Training days: {profile['days_per_week']}

Rules:
- Be realistic and safe
- Avoid generic plans
- Adapt to experience level
- Include workouts + diet

Return ONLY valid JSON:

{{
  "plan_type": "cut/bulk/recomp",
  "workouts": {{
    "push_day": [
      {{
        "exercise": "bench_press",
        "sets": [
          {{"reps": 10, "weight": 135}},
          {{"reps": 8, "weight": 135}}
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


# -------------------------
# PROMPT: ADJUSTMENT
# -------------------------
def build_adjustment_prompt(profile, plan, checkins, user_message, progress):
    return f"""
You are an adaptive fitness coach AI.

You manage a living training system.

USER MESSAGE:
{user_message}

CURRENT PLAN:
{json.dumps(plan, indent=2)}

CHECK-INS:
{json.dumps(checkins, indent=2)}

PROGRESS:
{json.dumps(progress, indent=2)}

PROFILE:
- Age: {profile['age']}
- Weight: {profile['weight']}
- Goal: {profile['goal']}
- Experience: {profile['experience']}
- Training days: {profile['days_per_week']}

RULES:
- Do NOT rewrite the whole plan unless necessary
- Be conservative with changes
- Only adjust when needed

Return STRICT JSON:

{{
  "decision": "keep | small_adjustment | major_adjustment",
  "workout_changes": {{}},
  "diet_changes": {{}},
  "reasoning": "",
  "confidence": 0.0
}}
"""


# -------------------------
# GENERATE PLAN
# -------------------------
def generate_ai_plan(profile):
    try:
        prompt = build_prompt(profile)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are CoachAI, a fitness planning AI."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        return safe_parse_ai_response(content)

    except Exception as e:
        return {
            "error": "ai_failure",
            "details": str(e)
        }

# -------------------------
# CHAT / ADJUSTMENT ENGINE
# -------------------------
def coach_chat(context, user_message, progress=None):
    try:
        prompt = build_adjustment_prompt(
            context["profile"],
            context["plan"],
            context["checkins"],
            user_message,
            progress
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are CoachAI, an adaptive fitness coach."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        return safe_parse_ai_response(content)

    except Exception as e:
        return {
            "error": "ai_chat_failure",
            "details": str(e)
        }