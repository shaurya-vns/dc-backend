# Utility functions
import base64
import os
from datetime import datetime
import jwt
from dc.settings import *

def generate_salt(length=32):
    return base64.b64encode(os.urandom(length)).decode('utf-8')

def check_password(hashedPassword, password):
    return hashedPassword == password

def encode_token(payload):
    payload['time'] = datetime.now().strftime("%H:%M:%S:%f")
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.DecodeError:
        return False
    
def store_token(phoneNumber, token):
    REDIS.rpush(phoneNumber, token)

def remove_token(phoneNumber, token):
    REDIS.lrem(phoneNumber, 0, token)

def check_password_match(hashedPassword, password):
    return hashedPassword == password