import os
from sqlalchemy import create_engine

SECRET_KEY = ')%2u{@y]kOP-};43i){r<2)'
DATABASE_URL = "postgresql+psycopg2://myuser:mypassword@localhost:5432/savannah"
SQLALCHEMY_TRACK_MODIFICATIONS = False
AFRICAS_TALKING_API_KEY = os.environ.get('AFRICAS_TALKING_API_KEY')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
AUTHORIZE_URL='https://dev-dvk7bu07pum1d5h0.us.auth0.com/authorize'
ACCESS_TOKEN_URL='https://dev-dvk7bu07pum1d5h0.us.auth0.com/oauth/token',


