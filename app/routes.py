from flask import Blueprint, redirect, request, url_for, session, jsonify, Flask, render_template
from flask_login import login_user, UserMixin, LoginManager, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode, quote_plus

from flask_sqlalchemy import SQLAlchemy
from app.models import CustomerOrder
from app import db
from config import AUTH0_CLIENT_ID, AUTH0_DOMAIN, AUTH0_CLIENT_SECRET, JWKS_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL, AFRICAS_TALKING_API_KEY, SQLALCHEMY_DATABASE_URI
import africastalking
import os

app = Flask(__name__)


bp = Blueprint('routes', __name__)

# Implement authentication and authorization via OpenID Connect
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User()

@bp.route('/')
def index():
    if not session.get('access_token'):
        return redirect('/login')
    return render_template('home.html')

oauth = OAuth(app)

auth0 = oauth.register(
    name='auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    jwks_uri=JWKS_URI,
    authorize_url=AUTHORIZE_URL,
    access_token_url=ACCESS_TOKEN_URL,
    client_kwargs={'scope': 'openid profile email'}
)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    state = os.urandom(16).hex()
    session['state'] = state
    return oauth.auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback', state=state)

@bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = auth0.authorize_access_token()
    session['access_token'] = token_info['access_token']
    return redirect('/order')

@bp.route('/logout')
def logout():
    session.clear()
    return render_template('home.html')

# Initialize Africa's Talking SMS
africastalking.initialize(username='sandbox', api_key=AFRICAS_TALKING_API_KEY)
sms = africastalking.SMS

@bp.route('/order')
def show_order_form():
    return render_template('order.html')

@bp.route('/orders', methods=['POST'])
def add_order():
    # Parse JSON data from the request
    data = request.json
    customer_id = data.get('customer_id')
    name = data.get('name')
    phone_number = data.get('phone_number')
    item = data.get('item')
    amount = data.get('amount')
    time = data.get('time')

    try:
        # Create the new order
        new_order = CustomerOrder(name=name, phone_number=phone_number, item=item, amount=amount, time=time)
        db.session.add(new_order)
        db.session.commit()

        # Send message upon successful order placement
        message = f"Hello! New order for {item} placed successfully. Amount: {amount}. Time {time}"
        response = sms.send(message, [phone_number])
        print(response)

        return jsonify({'message': 'Order added successfully'})
    except Exception as e:
        print(f"Failed to complete order process: {e}")
        return jsonify({'message': 'Failed to complete order process'}), 500