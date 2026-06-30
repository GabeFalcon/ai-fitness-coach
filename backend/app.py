from flask import Flask

from database.init_db import init_db

from routes.auth_routes import auth_bp
from routes.profile_routes import profile_bp
from routes.plan_routes import plan_bp
from routes.checkin_routes import checkin_bp
from routes.chat_routes import chat_bp
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    # initialize database tables
    init_db()

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(chat_bp)

    return app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)