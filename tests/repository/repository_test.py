from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from mocks.record_book import mock_data_record_book
from src.repository.record_book import RecordBookRepository


def test_should_save_record_book():
    table_record_book = mock_data_record_book()
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        repository: RecordBookRepository = RecordBookRepository(db_session=session)
        repository.save(table_record_book)
        session.add.assert_called_once_with(table_record_book)
