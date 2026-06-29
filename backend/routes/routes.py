from flask import Flask
from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.plan_routes import plan_bp
from routes.checkin_routes import checkin_bp
from routes.chat_routes import chat_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(chat_bp)

    return app
