import uuid

# In-memory user store
_USERS = {}


def create_user(email: str, password_hash: str, role: str) -> dict:
    user_id = str(uuid.uuid4())

    user = {
        "id": user_id,
        "email": email,
        "password_hash": password_hash,
        "role": role
    }

    _USERS[email] = user
    return user


def get_user_by_email(email: str) -> dict | None:
    return _USERS.get(email)