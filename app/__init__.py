from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Initialize SQLAlchemy database
db = SQLAlchemy()

def create_app():
    # Initialize Flask application instance
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    print("DATABASE_URL from environment:", os.getenv('DATABASE_URL'))

    # Load configuration from config.py
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    config_path = os.path.join(parent_dir, 'config.py')
    app.config.from_pyfile(config_path)

    # Configure SQLAlchemy database URI from environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with the Flask app instance
    db.init_app(app)

    # Import and register blueprints/routes
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

