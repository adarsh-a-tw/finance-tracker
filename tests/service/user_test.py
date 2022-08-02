import uuid
from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

import tables
from src.model.user import User
from src.service.user import UserService


def test_should_fetch_user_given_username():
    user_id: uuid.UUID = uuid.uuid4()
    username: str = "test_username"
    password: str = "test_password"
    email: str = "test_email"
    salt: str = "test_salt"

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        session.scalars().one_or_none.return_value = tables.User(id=user_id, username=username, password=password,
                                                                 email=email, salt=salt)
        service: UserService = UserService(db_session=session)
        user: User = service.fetch_user(username)

    assert user.username == username


@patch.object(User, 'check_password')
def test_should_return_valid_jwt_token_when_given_valid_username_and_password(mocked_check_password):
    user_id: str = str(uuid.uuid4())
    username: str = "test_username"
    password: str = "test_password"
    email: str = "test_email"
    salt: str = "test_salt"

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()
    mocked_check_password.return_value = True

    with mocked_session_class(mocked_engine) as session:
        session.scalars().one_or_none.return_value = tables.User(id=user_id, username=username, password=password,
                                                                 email=email, salt=salt)
        service: UserService = UserService(db_session=session)
        token: str = service.authenticate(username, password)

    mocked_check_password.assert_called_once_with(password)
    assert token is not None
