import uuid
from unittest.mock import patch, MagicMock, call

import tables
from src.model.user import User


def test_create_user():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = str(uuid.uuid4())

    user = User(user_id, username, email)

    assert user.username == username
    assert user.email == email


@patch('hashlib.sha512')
@patch('uuid.uuid4')
def test_should_set_password(mocked_uuid, mocked_hash_method):
    mocked_uuid.return_value = MagicMock(spec=uuid.UUID)
    sample_uuid = str(uuid.uuid4())
    salt_uuid = uuid.uuid4()

    username = "test_username"
    email = "test_email@domain.com"
    user_id = sample_uuid
    user = User(user_id, username, email)
    password = "test123"

    user.set_password(password)

    assert mocked_hash_method.called_once_with((password + salt_uuid.hex).encode('UTF-8'))


@patch('hashlib.sha512')
@patch('uuid.uuid4')
def test_should_check_password(mocked_uuid, mocked_hash_method):
    mocked_uuid.return_value = MagicMock(spec=uuid.UUID)
    sample_uuid = str(uuid.uuid4())
    salt_uuid = uuid.uuid4()
    hashed_password = MagicMock()
    mocked_hash_method.return_value = hashed_password
    username = "test_username"
    email = "test_email@domain.com"
    user_id = sample_uuid
    user = User(user_id, username, email)
    password = "test123"
    sample_uuid_hex__encode = (password + salt_uuid.hex).encode('UTF-8')
    user.set_password(password)

    assert user.check_password(password) is True

    assert [call(sample_uuid_hex__encode), call(sample_uuid_hex__encode)] == mocked_hash_method.call_args_list


def test_should_map_model_user_to_data_model():
    username = "test_username"
    email = "test_email@domain.com"
    password = "test123"
    user_id = str(uuid.uuid4())
    model_user = User(user_id, username, email)
    model_user.set_password(password)

    data_user: tables.User = model_user.data_model()

    assert data_user.id == model_user.id
    assert data_user.username == model_user.username
    assert data_user.email == model_user.email
    assert data_user.password == model_user._password  # pylint: disable=protected-access
    assert data_user.salt == model_user._salt  # pylint: disable=protected-access


def test_should_create_model_user_from_data_model():
    username = "test_username"
    email = "test_email@domain.com"
    password = "sample_password"
    salt = "sample_salt"
    user_id = str(uuid.uuid4())
    data_user: tables.User = tables.User(id=user_id, username=username, email=email, password=password, salt=salt)

    model_user: User = User.from_data_model(data_user)

    assert data_user.id == model_user.id
    assert data_user.username == model_user.username
    assert data_user.email == model_user.email
    assert data_user.password == model_user._password  # pylint: disable=protected-access
    assert data_user.salt == model_user._salt  # pylint: disable=protected-access
