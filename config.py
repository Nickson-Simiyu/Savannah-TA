import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Africa's Talking API credentials
AFRICAS_TALKING_USERNAME = 'your_username'
AFRICAS_TALKING_API_KEY = 'your_api_key'
