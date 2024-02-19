from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Import routes from routes.py
from app import bp as routes_bp
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
