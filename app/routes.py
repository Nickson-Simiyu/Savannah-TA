from flask import jsonify, request
from app import app, db
from app.models import Customer, Order
from flask import Blueprint, redirect, request, url_for, session, jsonify
from auth0.authentication import GetToken
from auth0.management import Auth0

from app import app

bp = Blueprint('routes', __name__)

# Initialize Auth0 SDK
auth0_domain = app.config.get('AUTH0_DOMAIN')
client_id = app.config.get('AUTH0_CLIENT_ID')
client_secret = app.config.get('AUTH0_CLIENT_SECRET')
auth0 = Auth0(auth0_domain, client_id, client_secret)
get_token = GetToken(auth0_domain)

# Route to login
@bp.route('/login')
def login():
    return redirect(get_token.authorization_url(redirect_uri='http://localhost:5000/callback'))

# Route to handle callback
@bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = get_token.exchange(authorization_code=code, redirect_uri='http://localhost:5000/callback')
    session['access_token'] = token_info['access_token']
    return redirect(url_for('profile'))

# Route to display user profile
@bp.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    userinfo = auth0.users.get('me')
    return f'Hello, {userinfo["name"]}'

# Route to logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



# Route to add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], code=data['code'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'})

# Route to add a new order
@app.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'], item=data['item'], amount=data['amount'], time=data['time'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order added successfully'})
