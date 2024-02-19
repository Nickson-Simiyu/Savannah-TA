from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access environment variables
africas_talking_api_key = os.environ.get('AFRICAS_TALKING_API_KEY')

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
config_path = os.path.join(parent_dir, 'config.py')
app.config.from_pyfile(config_path)

# Configure SQLAlchemy database URI from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy database
db = SQLAlchemy(app)

# Import routes and models
from app import routes, models
from  .routes import bp as routes_bp