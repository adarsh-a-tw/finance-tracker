import uuid
from unittest.mock import patch, MagicMock, call

from src.users.domain.user import User


def test_create_user():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = uuid.uuid4()

    user = User(user_id, username, email)

    assert user.username == username
    assert user.email == email


@patch('hashlib.sha512')
@patch('uuid.uuid4')
def test_should_set_password(mocked_uuid, mocked_hash_method):
    mocked_uuid.return_value = MagicMock(spec=uuid.UUID)
    sample_uuid = uuid.uuid4()

    username = "test_username"
    email = "test_email@domain.com"
    user_id = sample_uuid
    user = User(user_id, username, email)
    password = "test123"

    user.set_password(password)

    assert mocked_hash_method.called_once_with((password + sample_uuid.hex).encode('UTF-8'))


@patch('hashlib.sha512')
@patch('uuid.uuid4')
def test_should_check_password(mocked_uuid, mocked_hash_method):
    mocked_uuid.return_value = MagicMock(spec=uuid.UUID)
    sample_uuid = uuid.uuid4()
    hashed_password = MagicMock()
    mocked_hash_method.return_value = hashed_password
    username = "test_username"
    email = "test_email@domain.com"
    user_id = sample_uuid
    user = User(user_id, username, email)
    password = "test123"
    sample_uuid_hex__encode = (password + sample_uuid.hex).encode('UTF-8')
    user.set_password(password)

    assert user.check_password(password) is True

    assert [call(sample_uuid_hex__encode), call(sample_uuid_hex__encode)] == mocked_hash_method.call_args_list
