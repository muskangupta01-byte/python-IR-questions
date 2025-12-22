from passlib.hash import bcrypt

# In-memory user store
USERS = {}

def register_user(username, password):
    hashed_pw = bcrypt.hash(password)
    USERS[username] = hashed_pw

def authenticate_user(username, password):
    hashed_pw = USERS.get(username)
    if not hashed_pw:
        return None

    if bcrypt.verify(password, hashed_pw):
        return {"username": username}

    return None