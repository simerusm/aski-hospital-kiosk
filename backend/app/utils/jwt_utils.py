import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import os

# Get the JWT secret key from environment variable or use a default for development
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = timedelta(minutes=1)  # Token expires in 1 minute

def generate_token(user_id: int, ssn: str) -> str:
    """Generate a JWT token for a user."""
    payload = {
        'user_id': user_id,
        'ssn': ssn,
        'exp': datetime.now(timezone.utc) + JWT_EXPIRATION_DELTA,
        'iat': datetime.now(timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    """Decode a JWT token and return the payload."""
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')

def token_required(f):
    """Decorator to protect routes that require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode token and get user info
            payload = decode_token(token)
            # Add user info to request context
            request.user = payload
        except Exception as e:
            return jsonify({'message': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated 