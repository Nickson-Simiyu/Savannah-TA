from flask import Blueprint, redirect, request, url_for, session, jsonify, Flask, render_template
from flask_login import login_user, UserMixin, LoginManager, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from app.models import Customer, CustomerOrder
from app import db
from config import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, JWKS_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL, AFRICAS_TALKING_API_KEY, SQLALCHEMY_DATABASE_URI
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
    return "Hello World with Flask"

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
    return redirect('/login')


# Initialize Africa's Talking SMS
africastalking.initialize(username='sandbox', api_key=AFRICAS_TALKING_API_KEY)
sms = africastalking.SMS


@bp.route('/order')
def show_order_form():
    return render_template('order.html')

@bp.route('/sms_callback', methods=['POST'])
def sms_callback():
    print(request.method)
    print(request.form)
    if 'from' in request.form:
        sender = request.form['Nickson']
        print(f"SMS received from: {sender}")
    else:
        print("No 'from' key found in form data")
    return "Success", 201

@bp.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    customer_id = data.get('customer_id')
    item = data.get('item')
    amount = data.get('amount')
    time = data.get('time')

    # Check if the customer exists
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    # Create the new order
    new_order = CustomerOrder(customer_id=customer_id, item=item, amount=amount, time=time)
    db.session.add(new_order)
    db.session.commit()

    # Send SMS alert to the customer
    phone_number = customer.phone_number 
    message = f"Hello {customer.name}, your order for {item} has been successfully placed."
    try:
        response = sms.send(message, [phone_number])
        print(response)
        return jsonify({'message': 'Order added successfully and SMS sent'})
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return jsonify({'message': 'Order added successfully, but failed to send SMS'}), 500
