from auth_service import register_user, authenticate_user

def test_password_hashing():
    register_user("alice", "password123")
    user = authenticate_user("alice", "password123")
    assert user is not None

def test_invalid_password():
    register_user("bob", "secret")
    user = authenticate_user("bob", "wrong")
    assert user is None