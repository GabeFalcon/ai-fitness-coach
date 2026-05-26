# Create a blueprint  
from flask import Blueprint, request
import uuid
import random

routes_bp = Blueprint('main', __name__)


# Temporary data storage
users = {}

user_profiles = {}

# Define allowed data options
ALLOWED_GOALS = ["fat_loss", "muscle_gain", "maintenance", "fat_loss_and_muscle_gain"]

ALLOWED_EXPERIENCE = ["beginner", "intermediate", "advanced"]

@routes_bp.route("/")
def welcome():
    return "<p>Welcome to CoachAI</p>"

# See the status of the website
@routes_bp.route("/health")
def health():
    return {
        "status": "online",
        "version": "beta 0.1",
        "message": "hey you shouldn't be here user!",
        "app_name": "Coach AI"
    }

# Account Creation
@routes_bp.route("/signup", methods=["POST"])
def signup():
    global users

    user_data = request.get_json()

    if not user_data:
        return {"error": "no JSON provided"}, 400

    required_fields = ["email", "username", "password"]
    # Make sure each field has been submitted
    for field in required_fields:
        if field not in user_data:
            return {"error": f"missing field: {field}"}, 400

    # Make sure the email is valid
    for existing_user in users.values():
        if existing_user.get("email") == user_data["email"]:
            return {"error": "account with email exsits"}, 400
    
    user_id = str(uuid.uuid4())

    # Store the user data
    users[user_id] = {
        "user_id": user_id,
        "email": user_data["email"],
        "username": user_data["username"],
        "password": user_data["password"]
    }

    return {
    "message": "account created successfully",
    "user_id": user_id
    }

# Store user data
@routes_bp.route("/onboarding", methods=["POST"])
def onboarding():
    global user_profiles 

    data = request.get_json()

    # Ensure data exists
    if not data:
        return {"error": "no JSON provided"}, 400

    required_fields = ["age", "weight", "height", "days_per_week", "goal", "experience", "user_id"]
    
    for field in required_fields:
        if field not in data:
            return {"error": f"missing field: {field}"}, 400

    if data["goal"] not in ALLOWED_GOALS:
        return {"error": "invalid goal"}, 400
    
    if data["experience"] not in ALLOWED_EXPERIENCE:
        return {"error": "invalid experience"}, 400
    
    if data["user_id"] not in users:
        return {"error": "user does not exist"}, 400

    # Store the data
    user_profiles[data["user_id"]] = {
        "age": int(data["age"]),
        "weight": float(data["weight"]),
        "height": int(data["height"]),
        "days_per_week": int(data["days_per_week"]),
        "goal": data["goal"].lower(),
        "experience": data["experience"].lower()
    }

    return {
        "user_id": data["user_id"],
        "message": "data saved successfully",
        "stored_data": user_profiles[data["user_id"]]
    }

# Retrieve user data
@routes_bp.route("/profile", methods=["GET"])
def profile():
    user_id = request.args.get("user_id")

    if not user_id:
        return {"error": "missing user_id"}, 400

    if user_id not in user_profiles:
        return {"error": "profile not found"}, 404

    return {
        "user_id": user_id,
        "data": user_profiles[user_id]
    }

# AI Plan Generator
@routes_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json()

    if not data:
        return {"error": "no JSON provided"}, 400

    if "user_id" not in data:
        return {"error": "missing user_id"}, 400

    user_id = data["user_id"]

    if user_id not in user_profiles:
        return {"error": "profile not found"}, 404

    profile = user_profiles[user_id]

    experience = profile["experience"]
    goal = profile["goal"]

    # “AI personality layer” (this is what makes it feel alive)
    hooks = [
        "Based on your profile, here’s what I’d do if I were coaching you:",
        "I’ve analyzed your stats — this is your optimal starting path:",
        "Let’s build something sustainable for you:",
        "Here’s your personalized game plan:"
    ]

    hook = random.choice(hooks)

    def response(plan_type, workout, notes, diet):
        return {
            "message": hook,
            "plan_type": plan_type,
            "workout": workout,
            "notes": notes,
            "diet": diet
        }

    # -------------------
    # BEGINNER
    # -------------------
    if experience == "beginner":

        if goal == "fat_loss":
            return response(
                "fat_loss_beginner",
                "30–60 min cardio daily + step increase weekly",
                "Focus on consistency. Your body responds best to repetition right now.",
                "Start with ~300–500 calorie deficit depending on hunger + weight trend"
            )

        if goal == "fat_loss_and_muscle_gain":
            return response(
                "recomp_beginner",
                "3–4 full body sessions + light cardio after lifting",
                "You’re in recomposition mode — balance is key.",
                "Small deficit or maintenance calories depending on progress"
            )

        if goal == "muscle_gain":
            return response(
                "hypertrophy_beginner",
                "Full body 3–4x/week + progressive overload focus",
                "Form > weight. You’re building your foundation right now.",
                "Slight surplus recommended if strength is not increasing"
            )

    # -------------------
    # INTERMEDIATE
    # -------------------
    if experience == "intermediate":

        if goal == "fat_loss":
            return response(
                "fat_loss_intermediate",
                "4–5 day split + cardio 2–3x/week",
                "Now we optimize intensity, not just consistency.",
                "Moderate calorie deficit with high protein focus"
            )

        if goal == "fat_loss_and_muscle_gain":
            return response(
                "recomp_intermediate",
                "Upper/lower split + conditioning work",
                "You’re close to full recomposition efficiency.",
                "Cycle between maintenance and slight deficit"
            )

        if goal == "muscle_gain":
            return response(
                "hypertrophy_intermediate",
                "Push/pull/legs + progressive overload cycles",
                "Volume + recovery is your new bottleneck.",
                "Slight calorie surplus with performance tracking"
            )

    # -------------------
    # ADVANCED
    # -------------------
    if experience == "advanced":

        if goal == "fat_loss":
            return response(
                "cutting_advanced",
                "High volume split + structured cardio blocks",
                "We’re now optimizing muscle retention while cutting.",
                "Controlled deficit with refeeds if needed"
            )

        if goal == "fat_loss_and_muscle_gain":
            return response(
                "recomp_advanced",
                "Periodized training + HIIT integration",
                "This is precision work now — small adjustments matter.",
                "Calories cycled based on training days"
            )

        if goal == "muscle_gain":
            return response(
                "hypertrophy_advanced",
                "High frequency split + progressive overload cycles",
                "We push performance ceilings here.",
                "Lean surplus with performance-based adjustments"
            )

    return response(
        "default",
        "Balanced training plan",
        "Not enough signal — starting with a general plan",
        "Moderate intake based on goals"
    )