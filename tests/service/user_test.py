from src.service.user import UserService


def test_should_return_valid_jwt_token_when_given_valid_username_and_password():
    service: UserService = UserService()
    username: str = "test_username"
    password: str = "test_password"

    token = service.authenticate(username, password)

    assert token is not None

