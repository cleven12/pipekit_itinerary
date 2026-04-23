from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    from app.blueprints.itinerary import itinerary_bp
    app.register_blueprint(itinerary_bp)

    return app
