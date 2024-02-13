from functools import wraps
from flask import request, jsonify

# Mocked function for demo, replace with actual OpenID Connect integration
def verify_token(token):
    # Mocked implementation, always returns True
    return True

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Authorization token is missing'}), 401
        if not verify_token(token):
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated
