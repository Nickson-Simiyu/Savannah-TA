from flask import Blueprint, redirect, request, url_for, session, jsonify, Flask
from flask_login import login_user, UserMixin, LoginManager, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from app.models import Customer, Order
from app import db
from config import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, JWKS_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL, AFRICAS_TALKING_API_KEY
import africastalking
import os

app = Flask(__name__)

bp = Blueprint('routes', __name__)

# Implement authentication and authorization via OpenID Connect
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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
    return redirect('/')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# When an order is added, send the customer an SMS alerting them
@bp.route('/sms_callback', methods=['POST'])
def sms_callback():
    print(request.method)
    print(request.form)
    if 'from' in request.form:
        sender = request.form['from']
        print(f"SMS received from: {sender}")
    else:
        print("No 'from' key found in form data")
    return "Success", 201

# Endpoint for adding a new order
@bp.route('/orders', methods=['POST'])
@login_required
def add_order():
    data = request.json
    customer_id = data.get('customer_id')
    item = data.get('item')
    amount = data.get('amount')
    time = data.get('time')

    # Create a new order object and add it to the database
    new_order = Order(customer_id=customer_id, item=item, amount=amount, time=time)
    db.session.add(new_order)
    db.session.commit()

    # Retrieve customer's phone number from the database
    customer = Customer.query.get(customer_id)
    phone_number = customer.phone_number 

    # Send SMS alert to the customer
    message = f"Hello {customer.name}, your order for {item} has been successfully placed."
    try:
        response = sms.send(message, [phone_number])
        print(response)
        return jsonify({'message': 'Order added successfully and SMS sent'})
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return jsonify({'message': 'Order added successfully, but failed to send SMS'}), 500