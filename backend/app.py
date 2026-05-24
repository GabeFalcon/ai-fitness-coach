from flask import Flask
from routes.routes import routes_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(routes_bp, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)