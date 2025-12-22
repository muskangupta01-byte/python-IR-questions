import time
import uuid
from flask import Blueprint, request, jsonify
from auth_service import register_user, authenticate_user
from jwt_utils import generate_jwt
from email_queue import publish_event
from logger import log_info, log_warn

auth_bp = Blueprint("auth", __name__)

# Authentication = verifying identity (login)
# Authorization = checking permissions after login
# OAuth2 would replace username/password login with external identity providers

@auth_bp.route("/register", methods=["POST"])
def register():
    start = time.time()
    data = request.json
    register_user(data["username"], data["password"])
    publish_event("WELCOME_EMAIL", data["username"])

    log_info("/register", "SUCCESS", start)
    return jsonify({"message": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    start = time.time()
    data = request.json
    user = authenticate_user(data["username"], data["password"])

    if not user:
        log_warn("/login", "INVALID_CREDENTIALS", start)
        return jsonify({"error": "Unauthorized"}), 401

    token = generate_jwt(user)
    log_info("/login", "SUCCESS", start)

    return jsonify({"token": token}), 200