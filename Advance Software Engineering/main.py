from auth_controller import (
    register,
    login,
    oauth_login,
    access_admin_resource
)

def main():
    print("---- User Registration ----")
    print(register("user@example.com", "password123"))

    print("\n---- User Login ----")
    login_response = login("user@example.com", "password123")
    user_token = login_response["token"]
    print("JWT issued")

    print("\n---- Access Admin Resource (USER) ----")
    try:
        print(access_admin_resource(user_token))
    except Exception as e:
        print(e)

    print("\n---- OAuth Login ----")
    oauth_response = oauth_login("valid-oauth-code")
    admin_token = oauth_response["token"]
    print("OAuth JWT issued")

    print("\n---- Access Admin Resource (ADMIN) ----")
    print(access_admin_resource(admin_token))


if __name__ == "__main__":
    main()


#expected output
"""
---- User Registration ----
{'message': 'User registered successfully', 'user_id': '...'}

---- User Login ----
JWT issued

---- Access Admin Resource (USER) ----
Access denied: ADMIN role required

---- OAuth Login ----
OAuth JWT issued

---- Access Admin Resource (ADMIN) ----
Admin resource accessed
"""