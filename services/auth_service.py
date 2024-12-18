import requests
from flask import request, jsonify
from functools import wraps
from config import Config
class AuthService:
    @staticmethod
    def validate_token(token):
        try:
            # Validate token with User Account Service
            response = requests.get(
                f"{Config.USER_SERVICE_URL}/api/users/profile", 
                headers={'Authorization': f'Bearer {token}'}
            )
            
            if response.status_code == 200:
                # Decode token to get user information
                user_data = response.json()
                return user_data
            return None
        except Exception as e:
            return None

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            
            # Check if token is in Authorization header
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]
            
            if not token:
                return jsonify({'error': 'Authentication token is missing'}), 401
            
            user = AuthService.validate_token(token)
            if not user:
                return jsonify({'error': 'Invalid token'}), 401
            
            return f(user, *args, **kwargs)
        
        return decorated