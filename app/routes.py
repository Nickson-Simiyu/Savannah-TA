from flask import Blueprint, redirect, request, url_for, session, jsonify, Flask
from flask_login import login_user
from app import db
from app.models import Customer, Order
from auth0.authentication import GetToken
from auth0.management import Auth0
from authlib.integrations.base_client.errors import OAuthError
from authlib.integrations.requests_client import OAuth2Session
from authlib.integrations.flask_client import OAuth
from config import SECRET_KEY, DATABASE_URL, SQLALCHEMY_TRACK_MODIFICATIONS, AFRICAS_TALKING_API_KEY, AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTHORIZE_URL, ACCESS_TOKEN_URL
import secrets

bp = Blueprint('routes', __name__)

app = Flask(__name__)
oauth = OAuth(app)


# Configure OAuth with Auth0 endpoints
oauth.register(
    name='auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    authorize_url=AUTHORIZE_URL,
    access_token_url=ACCESS_TOKEN_URL,
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@app.route('/')
def index():
    return 'Welcome to the index page'

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Generate a random state parameter
    state = secrets.token_urlsafe(16)
    
    # Store the state parameter in the session
    session['state'] = state
    
    redirect_uri = url_for('routes.callback', _external=True)
    return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri, state=state)

@bp.route('/callback')
def callback():
    # Ensure CSRF protection by checking state parameter
    received_state = request.args.get('state')
    expected_state = session.get('state')

    if received_state is None or received_state != expected_state:
        return f'Invalid state parameter. Received: {received_state}, Expected: {expected_state}', 400

    # Exchange authorization code for access token
    code = request.args.get('code')
    if code is None:
        return 'Authorization code is missing', 400

    # Fetch token using access_token_url registered during OAuth configuration
    token = oauth.auth0._fetch_token(token_url=oauth.auth0.access_token_url, code=code)

    # Store access token or process as needed
    session['access_token'] = token['access_token']

    # Redirect to a protected resource or profile page
    return redirect('/')








@bp.route('/profile', methods=['GET', 'POST'])
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
@bp.route('/customers', methods=['GET', 'POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], code=data['code'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'})

# Route to add a new order
@bp.route('/orders', methods=['GET', 'POST'])
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
