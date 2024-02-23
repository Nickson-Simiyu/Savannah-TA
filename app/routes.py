from flask import Blueprint, redirect, request, url_for, session, jsonify, Flask
from flask_login import login_user, UserMixin, LoginManager, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from authlib.integrations.flask_client import OAuth
from app.models import Customer, Order
from app import db
from config import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, JWKS_URI, AUTHORIZE_URL, ACCESS_TOKEN_URL
import os

app = Flask(__name__)

bp = Blueprint('routes', __name__)

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

@bp.route('/')
def index():
    return "Hello World with Flask"

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
@login_required
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

@bp.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], code=data['code'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'})

@bp.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'], item=data['item'], amount=data['amount'], time=data['time'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order added successfully'})
