import tables
from src.model.user import User


def mock_data_user():
    user_id: str = "mock_uuid"
    username: str = "test_username"
    password: str = "test_password"
    email: str = "test_email"
    salt: str = "test_salt"

    return tables.User(id=user_id, username=username,
                       password=password,
                       email=email, salt=salt)


def mock_model_user():
    user_id: str = "mock_uuid"
    username: str = "test_username"
    password: str = "test_password"
    email: str = "test_email"
    salt: str = "test_salt"

    return User(id=user_id, username=username,
                _password=password,
                email=email, _salt=salt)
