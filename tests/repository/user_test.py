from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from mocks.user import mock_data_user
import tables
from src.repository.user import UserRepository


def test_should_save_user():
    data_user = mock_data_user()
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        repository: UserRepository = UserRepository(db_session=session)
        repository.save(data_user)
        session.add.assert_called_once_with(data_user)


def test_should_fetch_user_given_username():
    username: str = "test_username"

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        data_user = mock_data_user()
        session.scalars().one_or_none.return_value = data_user
        repository: UserRepository = UserRepository(db_session=session)
        fetched_user: tables.User = repository.fetch_user(username)

    assert data_user == fetched_user
