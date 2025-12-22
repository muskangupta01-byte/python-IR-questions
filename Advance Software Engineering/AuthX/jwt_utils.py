import jwt
import datetime

SECRET = "secret-key"

def generate_jwt(user):
    payload = {
        "sub": user["username"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")