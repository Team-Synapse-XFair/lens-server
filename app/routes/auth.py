from flask import Blueprint, jsonify, request
from app.services.mongo import getUser
from argon2 import PasswordHasher
import jwt
from datetime import datetime, timedelta
import os
from app.schemas.templates import UserTemplate
from app.services.mongo import saveUser
from app.services.auth import verify_password, hash_password

authBP = Blueprint("auth", __name__, url_prefix="/auth")

@authBP.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = getUser(data.get("email"))
    
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401
    
    if not verify_password(user['hashed_password'], data.get("password")):
        return jsonify({"message": "Invalid email or password"}), 401

    secretKey = os.getenv("JWT_SECRET", "OkayIGuessThisIsSecureEnoughForDev")

    payload = {
        'user_id': str(user["_id"]),
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.now() + timedelta(hours=24)
    }
    token = jwt.encode(payload, secretKey, algorithm='HS256')
    print(f"Generated JWT for user {user['email']}")

    response = {
        "success": True,
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "username": user['username'],
            "email": user['email'],
        }
    }

    return jsonify(response), 200, {'Content-Type': 'application/json'}
    
@authBP.route("/register", methods=["POST"])
def register():
    ## TODO Implement user registration logic
    data = request.get_json()

    if (not data.get("email") or
        not data.get("username") or
        not data.get("password") or
        not data.get("name")
    ):
        return jsonify({"message": "Missing required fields"}), 400

    user = UserTemplate()
    user["email"] = data["email"]
    user["username"] = data["username"]
    user["name"] = data["name"]
    user["hashed_password"] = hash_password(data["password"])
    user["role"] = "citizen" ## NOTE Default role
    user["created_at"] = datetime.now()
    user["updated_at"] = datetime.now()

    saveUser(user)

    return jsonify({ "success": True, "message": "Registered Successfuly" }), 201