import jwt
import json
from passlib.hash import bcrypt
from datetime import datetime, timedelta

# -----------------------------
# In-memory user store
# (passwords are bcrypt hashed)
# -----------------------------
USERS = {
    "alice": bcrypt.hash("alice123"),
    "bob": bcrypt.hash("bob123")
}

JWT_SECRET = "secret-key"
JWT_ALGO = "HS256"


def log_event(event, username, status):
    """
    Structured logging (JSON-style).
    Never log passwords or tokens.
    """
    print(json.dumps({
        "event": event,
        "username": username,
        "status": status,
        "timestamp": datetime.utcnow().isoformat()
    }))


def generate_jwt(username):
    """
    JWT represents successful authentication.
    Authorization decisions are made AFTER this step.
    """
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)


def login_user(username, password):
    """
    Authentication vs Authorization:
    - Authentication: verifying who the user is (done here)
    - Authorization: checking what the user can access (done later)

    OAuth2 note:
    - In real systems, this function would be replaced by an OAuth2
      Authorization Server (Google, Auth0, Keycloak, etc.)
    """

    log_event("LOGIN_ATTEMPT", username, "STARTED")

    hashed_password = USERS.get(username)
    if not hashed_password:
        log_event("LOGIN_ATTEMPT", username, "FAILED")
        return None

    if not bcrypt.verify(password, hashed_password):
        log_event("LOGIN_ATTEMPT", username, "FAILED")
        return None

    token = generate_jwt(username)
    log_event("LOGIN_ATTEMPT", username, "SUCCESS")
    return token


# -----------------------------
# Example Usage
# (passwords are bcrypt hashed)
# -----------------------------
# token = login_user("alice", "alice123")
# print(token)