def exchange_code_for_user(code: str) -> dict:
    """
    Simulated OAuth provider.
    In real life this would call Google/GitHub.
    """
    if code != "valid-oauth-code":
        raise Exception("Invalid OAuth code")

    return {
        "email": "oauth_user@example.com",
        "role": "ADMIN"
    }