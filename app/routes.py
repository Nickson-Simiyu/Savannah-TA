from flask import Blueprint, redirect, request, url_for, session, jsonify, Flask
from app import db
from app.models import Customer, Order
from auth0.authentication import GetToken
from auth0.management import Auth0
from authlib.integrations.flask_client import OAuth
from config import SECRET_KEY, DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS, AFRICAS_TALKING_API_KEY, AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTHORIZE_URL

bp = Blueprint('routes', __name__)

app = Flask(__name__)
oauth = OAuth(app)

# Configure OAuth with Auth0 endpoints
oauth.register(
    name='auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    authorize_url=AUTHORIZE_URL,
    access_token_url='https://dev-dvk7bu07pum1d5h0.us.auth0.com/oauth/token',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@app.route('/')
def index():
    return 'Welcome to the index page'

@bp.route('/login')
def login():
    redirect_uri = url_for('routes.callback', _external=True)
    return oauth.auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

@bp.route('/callback')
def callback():
    token = oauth.auth0.authorize_access_token()
    userinfo = oauth.auth0.parse_id_token(token)
    session['access_token'] = token['access_token']
    return redirect(url_for('routes.profile'))

@bp.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('routes.login'))

    userinfo = oauth.auth0.get('userinfo')
    return f'Hello, {userinfo.json()["name"]}'

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))

# Route to add a new customer
@bp.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], code=data['code'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'})

# Route to add a new order
@bp.route('/orders', methods=['POST'])
def add_order():
    data = request.json
    new_order = Order(customer_id=data['customer_id'], item=data['item'], amount=data['amount'], time=data['time'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order added successfully'})

# Register blueprint with Flask app
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
