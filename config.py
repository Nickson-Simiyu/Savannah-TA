import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://myuser:mypassword@localhost:5432/savannah'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AFRICAS_TALKING_API_KEY = os.environ.get('AFRICAS_TALKING_API_KEY')