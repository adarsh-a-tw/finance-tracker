import uuid

from users.domain.user import User


def test_create_user():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = uuid.uuid4()

    user = User(user_id, username, email)

    assert user.username == username


def test_set_password():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = uuid.uuid4()
    user = User(user_id, username, email)
    password = "test123"

    user.set_password(password)

    assert user.check_password(password) is True
