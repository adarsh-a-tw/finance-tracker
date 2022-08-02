import uuid
from unittest.mock import patch, MagicMock, call

from sqlalchemy.orm import Session

import tables
from src.model.user import User


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


def test_should_map_domain_user_to_data_model():
    username = "test_username"
    email = "test_email@domain.com"
    password = "test123"
    user_id = uuid.uuid4()
    domain_user = User(user_id, username, email)
    domain_user.set_password(password)

    data_user: tables.User = domain_user.data_model()

    assert data_user.id == domain_user.id
    assert data_user.username == domain_user.username
    assert data_user.email == domain_user.email
    assert data_user.password == domain_user._password
    assert data_user.salt == domain_user._salt


def test_should_create_domain_user_from_data_model():
    username = "test_username"
    email = "test_email@domain.com"
    password = "sample_password"
    salt = "sample_salt"
    user_id = uuid.uuid4()
    data_user: tables.User = tables.User(id=user_id, username=username, email=email, password=password, salt=salt)

    domain_user: User = User.from_data_model(data_user)

    assert data_user.id == domain_user.id
    assert data_user.username == domain_user.username
    assert data_user.email == domain_user.email
    assert data_user.password == domain_user._password
    assert data_user.salt == domain_user._salt


def test_should_save_user_to_db():
    mocked_session_class = MagicMock(spec=Session)
    username = "test_username"
    email = "test_email@domain.com"
    password = "test123"
    user_id = uuid.uuid4()
    domain_user = User(user_id, username, email)
    domain_user.set_password(password)
    data_user: tables.User = tables.User(id=user_id, username=username, email=email,
                                         password=domain_user._password,
                                         salt=domain_user._salt)

    with mocked_session_class(MagicMock()) as session:
        domain_user.save(session)
        session.commit()
        session.add.assert_called_once()
        assert session.add.call_args[0][0] == data_user


def test_should_fetch_user_from_db_given_username():
    mocked_session_class = MagicMock(spec=Session)
    username = "test_username"
    email = "test_email@domain.com"
    password = "test123"
    user_id = uuid.uuid4()
    domain_user = User(user_id, username, email)
    domain_user.set_password(password)
    data_user: tables.User = tables.User(id=user_id, username=username, email=email,
                                         password=domain_user._password,
                                         salt=domain_user._salt)

    with mocked_session_class(MagicMock()) as session:
        domain_user.save(session)
        session.commit()
        session.add.assert_called_once()
        assert session.add.call_args[0][0] == data_user
