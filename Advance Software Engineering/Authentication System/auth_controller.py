from password_utils import hash_password, verify_password
from user_service import create_user, get_user_by_email
from jwt_utils import generate_jwt, verify_jwt
from oauth_service import exchange_code_for_user


def register(email: str, password: str) -> dict:
    if get_user_by_email(email):
        raise Exception("User already exists")

    password_hash = hash_password(password)
    user = create_user(email, password_hash, role="USER")

    return {"message": "User registered successfully", "user_id": user["id"]}


def login(email: str, password: str) -> dict:
    user = get_user_by_email(email)
    if not user:
        raise Exception("Invalid credentials")

    if not verify_password(password, user["password_hash"]):
        raise Exception("Invalid credentials")

    token = generate_jwt(user["id"], user["role"])
    return {"token": token}


def oauth_login(code: str) -> dict:
    oauth_user = exchange_code_for_user(code)

    user = get_user_by_email(oauth_user["email"])
    if not user:
        user = create_user(
            oauth_user["email"],
            password_hash="OAUTH_USER",
            role=oauth_user["role"]
        )

    token = generate_jwt(user["id"], user["role"])
    return {"token": token}


def access_admin_resource(token: str) -> str:
    payload = verify_jwt(token)

    if payload["role"] != "ADMIN":
        raise Exception("Access denied: ADMIN role required")

    return "Admin resource accessed"