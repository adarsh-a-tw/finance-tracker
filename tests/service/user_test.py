from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from mocks.user import mock_model_user, mock_data_user
from src.exceptions import InvalidCredentialsException
from src.model.user import User
from src.repository.user import UserRepository
from src.service.user import UserService


@patch('src.service.user.UserRepository')
def test_should_fetch_user_given_username(mocked_user_repository):
    username: str = "test_username"

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    mocked_user_repository_instance = MagicMock(spec=UserRepository)
    mocked_user_repository_instance.fetch_user.return_value = mock_data_user()
    mocked_user_repository.return_value = mocked_user_repository_instance

    with mocked_session_class(mocked_engine) as session:
        service: UserService = UserService(db_session=session)
        user: User = service.fetch_user(username)

    mocked_user_repository_instance.fetch_user.assert_called_once_with(username)
    assert user.username == username


@patch.object(User, 'check_password')
@patch('src.service.user.UserRepository')
def test_should_return_valid_jwt_token_when_given_valid_username_and_password(mocked_user_repository,
                                                                              mocked_check_password):
    username: str = "test_username"
    password: str = "test_password"

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()
    mocked_check_password.return_value = True

    mocked_user_repository_instance = MagicMock(spec=UserRepository)
    mocked_user_repository_instance.fetch_user.return_value = mock_data_user()
    mocked_user_repository.return_value = mocked_user_repository_instance

    with mocked_session_class(mocked_engine) as session:
        service: UserService = UserService(db_session=session)
        token: str = service.authenticate(username, password)

    mocked_check_password.assert_called_once_with(password)
    assert token is not None


@patch.object(User, 'check_password')
@patch('src.service.user.UserRepository')
def test_should_raise_exception_when_given_invalid_username_or_password(mocked_user_repository, mocked_check_password):
    username: str = "test_username"
    password: str = "test_password"

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()
    mocked_check_password.return_value = False

    mocked_user_repository_instance = MagicMock(spec=UserRepository)
    mocked_user_repository_instance.fetch_user.return_value = mock_data_user()
    mocked_user_repository.return_value = mocked_user_repository_instance

    with mocked_session_class(mocked_engine) as session:
        service: UserService = UserService(db_session=session)

        with pytest.raises(InvalidCredentialsException):
            service.authenticate(username, password)

    mocked_check_password.assert_called_once_with(password)


@patch('src.service.user.UserRepository')
def test_should_save_user(mocked_user_repository):
    user = mock_model_user()

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    mocked_user_repository_instance = MagicMock(spec=UserRepository)
    mocked_user_repository.return_value = mocked_user_repository_instance

    with mocked_session_class(mocked_engine) as session:
        service: UserService = UserService(session)
        service.save_user(user)

    mocked_user_repository_instance.save.assert_called_once_with(mock_data_user())
