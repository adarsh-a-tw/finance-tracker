from unittest.mock import MagicMock, patch

from sqlalchemy.orm import Session

from mocks.user import mock_model_user
from src.model.record_book import RecordBook as ModelRecordBook
from src.repository.record_book import RecordBookRepository
from src.repository.user import UserRepository
from src.service.record_book import RecordBookService


@patch('src.service.record_book.UserService')
@patch('src.service.record_book.RecordBookRepository')
def test_should_create_record_book_given_name_and_user(mocked_record_book_repository, mocked_user_service):
    name = "Test Record Book"
    username = "test_username"
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    mocked_user_service_instance = MagicMock(spec=UserRepository)
    mocked_user_service_instance.fetch_user.return_value = mock_model_user()
    mocked_user_service.return_value = mocked_user_service_instance

    mocked_record_book_repository_instance = MagicMock(spec=RecordBookRepository)
    mocked_record_book_repository.return_value = mocked_record_book_repository_instance

    with mocked_session_class(mocked_engine) as session:
        record_book_service = RecordBookService(session)
        record_book: ModelRecordBook = record_book_service.create_record_book(name, username)
        mocked_user_service_instance.fetch_user.assert_called_with(username)
        mocked_record_book_repository_instance.save.assert_called()

    assert isinstance(record_book, ModelRecordBook)
