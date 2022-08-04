from mocks.user import mock_model_user, mock_data_user
from src.model.record_book import RecordBook as ModelRecordBook
from src.model.user import User as ModelUser
import tables


def mock_data_record_book():
    name: str = "test_book"
    user_id: str = mock_data_user().id
    record_book_id: str = "mock_record_book_id"

    return tables.RecordBook(id=record_book_id, name=name, user_id=user_id, user=mock_data_user())


def mock_model_record_book():
    name: str = "test_book"
    user: ModelUser = mock_model_user()
    record_book_id: str = "mock_record_book_id"

    return ModelRecordBook(record_book_id, name, user)
