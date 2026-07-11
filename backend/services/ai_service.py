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

Allowed splits:
- "PPL"
- "Upper_Lower"
- "Full_Body"
- "Hybrid"
- "Custom"

Return ONLY valid JSON:

{
  "plan_type": "bulk",
  "split": "Upper_Lower",
  "schedule": [
    {
      "name": "Upper A",
      "focus": "upper",
      "exercises": []
    },
    {
      "name": "Lower A",
      "focus": "lower",
      "exercises": []
    }
  ],
  "diet": {
    "calories": 2500,
    "protein": 180,
    "carbs": 220,
    "fat": 65
  }
}
"""


# -------------------------
# PROMPT: ADJUSTMENT
# -------------------------
def build_adjustment_prompt(profile, plan, checkins, user_message, progress):
    return f"""
You are an adaptive fitness coach AI.

You manage a living training system.

The current program is assumed to be good.

Do NOT modify the workout or diet unless there is strong evidence that the current plan is no longer appropriate.

Prefer coaching advice over program changes.

A single bad workout is NOT enough reason to modify the plan.

A plateau should first be addressed with coaching cues (sleep, nutrition, technique, recovery, effort).

Only change exercises or split after repeated evidence that simpler interventions have failed.

Preserve as much of the existing program as possible.

USER MESSAGE:
{user_message}

CURRENT PLAN:
{json.dumps(plan or {"note": "no existing plan"}, indent=2)}

CHECK-INS:
{json.dumps(checkins[-7:], indent=2)}

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

STRICT PATCH FORMAT:

You are editing an existing JSON object.

You MUST NOT:
- create new top-level workout categories
- rename workout days
- restructure the plan

You MAY ONLY:
- add exercises inside existing days
- modify sets/reps/weights

Return STRICT JSON:
Example-
{{
  "decision": "keep | small_adjustment | major_adjustment",
  "workout_changes": {{{
      "action":"replace_exercise",
      "day":"Push A",
      "old":"Bench Press",
      "new":"Incline Bench Press"
    },}},
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
def coach_chat(context, user_message, progress):
    try:
        profile = context.get("profile", {})
        plan = context.get("plan", {})
        checkins = context.get("checkins", [])

        prompt = build_adjustment_prompt(
            profile,
            plan,
            checkins,
            user_message,
            progress
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are CoachAI, an adaptive fitness coach."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    except Exception as e:
        return {
            "error": "ai_chat_failure",
            "details": str(e)
        }