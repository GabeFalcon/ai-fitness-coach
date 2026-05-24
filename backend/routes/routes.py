# Create a blueprint  
from flask import Blueprint

routes_bp = Blueprint('main', __name__)


@routes_bp.route("/")
def welcome():
    return "<p>Welcome to CoachAI</p>"

# JSON that stores data of users?
@routes_bp.route("/health")
def health():
    return {
        "status": "online",
        "version": "beta 0.1",
        "message": "hey you shouldn't be here user!",
        "app_name": "Coach AI"
    }