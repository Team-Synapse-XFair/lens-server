import jwt
import os
from datetime import datetime, timedelta
from argon2 import PasswordHasher

def verify_token(token):
    JWT_SECRET = os.getenv("JWT_SECRET", "OkayIGuessThisIsSecureEnoughForDev")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

def hash_password(password):
    
    passHasher = PasswordHasher(parallelism=1, time_cost=2, memory_cost=19456)
    return passHasher.hash(password)

def verify_password(hashed_password, plain_password):
    passHasher = PasswordHasher(parallelism=1, time_cost=2, memory_cost=19456)
    try:
        passHasher.verify(hashed_password, plain_password)
        return True
    except:
        return False
    
def generate_jwt(user_id, email, role, hours_valid=24):
    JWT_SECRET = os.getenv("JWT_SECRET", "OkayIGuessThisIsSecureEnoughForDev")
    payload = {
        'user_id': str(user_id),
        'email': email,
        'role': role,
        'exp': datetime.now() + timedelta(hours=hours_valid)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token