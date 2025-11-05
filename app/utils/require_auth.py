from functools import wraps
from flask import request, jsonify
from app.services.auth import verify_token

def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return jsonify({"message": "Unauthorized"}), 403

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"message": "Invalid credentials"}), 401

        payload = verify_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token"}), 401

        request.user = payload
        return f(*args, **kwargs)
    return decorated_function