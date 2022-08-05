import uuid
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


def test_should_fetch_record_book():
    table_record_book = mock_data_record_book()
    record_book_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        session.scalars().one_or_none.return_value = table_record_book
        repository: RecordBookRepository = RecordBookRepository(db_session=session)
        record_book = repository.fetch_record_book(record_book_id, user_id)
        session.scalars().one_or_none.assert_called_once()
        assert record_book == table_record_book


def test_should_update_record_book_balance():
    table_record_book = mock_data_record_book()
    record_book_id = str(uuid.uuid4())
    new_balance = 100
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        session.scalars().one_or_none.return_value = table_record_book
        repository: RecordBookRepository = RecordBookRepository(db_session=session)
        updated_record_book = repository.update_net_balance_and_tags(record_book_id, new_balance,
                                                                     table_record_book.tag_map)
        session.scalars().one_or_none.assert_called_once()
        assert updated_record_book.net_balance == new_balance


def test_should_fetch_record_books():
    table_record_books = [mock_data_record_book()]
    user_id = str(uuid.uuid4())
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        session.scalars().all.return_value = table_record_books
        repository: RecordBookRepository = RecordBookRepository(db_session=session)
        record_books = repository.fetch_record_books(user_id)
        session.scalars().all.assert_called_once()
        assert record_books == table_record_books
