from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


# Initialize SQLAlchemy database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    migrate = Migrate(app, db)
    
    # Load environment variables from .env file
    load_dotenv()

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
