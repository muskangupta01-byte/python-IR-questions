from app import app
from auth_service import register_user
from unittest.mock import patch

client = app.test_client()

def test_login_success():
    register_user("test", "pass")

    with patch("jwt_utils.generate_jwt") as mock_jwt:
        mock_jwt.return_value = "fake-token"
        response = client.post("/login", json={
            "username": "test",
            "password": "pass"
        })

    assert response.status_code == 200
    assert "token" in response.json