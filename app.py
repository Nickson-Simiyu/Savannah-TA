from flask import Flask, redirect, request, url_for, session
from auth0.authentication import GetToken
from auth0.management import Auth0
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Initialize Auth0 SDK
auth0_domain = os.environ.get('AUTH0_DOMAIN')
client_id = os.environ.get('AUTH0_CLIENT_ID')
client_secret = os.environ.get('AUTH0_CLIENT_SECRET')
auth0 = Auth0(auth0_domain, client_id, client_secret)
get_token = GetToken(auth0_domain)

@app.route('/login')
def login():
    return redirect(get_token.authorization_url(redirect_uri='http://localhost:5000/callback'))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = get_token.exchange(authorization_code=code, redirect_uri='http://localhost:5000/callback')
    session['access_token'] = token_info['access_token']
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    userinfo = auth0.users.get('me')
    return f'Hello, {userinfo["name"]}'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
