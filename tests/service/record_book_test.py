import uuid
from typing import List
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from mocks.record_book import mock_model_record_book, mock_data_record_book
from mocks.user import mock_model_user
from exceptions import UserNotFoundException, RecordBookNotFoundException
from src.repository.record import RecordRepository
from src.model.record_type import RecordType
from src.model.record_book import RecordBook as ModelRecordBook
from src.model.record import Record as ModelRecord
from src.repository.record_book import RecordBookRepository
from src.repository.user import UserRepository
from src.service.record_book import RecordBookService

import tables


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


@patch('src.service.record_book.UserService')
@patch('src.service.record_book.RecordBookRepository')
@patch('src.service.record_book.RecordRepository')
def test_should_create_record_given_record_book_id_and_username(mocked_record_repository, mocked_record_book_repository,
                                                                mocked_user_service):
    record_book_id = mock_model_record_book().id
    username = mock_model_user().username
    note = "Sample Expense Record"
    amount = 20.92
    record_type = RecordType.EXPENSE
    tags = ["test_tag_1"]

    mocked_user_service_instance = MagicMock(spec=UserRepository)
    mocked_user_service_instance.fetch_user.return_value = mock_model_user()
    mocked_user_service.return_value = mocked_user_service_instance

    mocked_record_book_repository_instance = MagicMock(spec=RecordBookRepository)
    mocked_record_book_repository_instance.fetch_record_book.return_value = mock_data_record_book()
    mocked_record_book_repository.return_value = mocked_record_book_repository_instance

    mocked_record_repository_instance = MagicMock(spec=RecordRepository)
    mocked_record_repository.return_value = mocked_record_repository_instance

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        record_book_service = RecordBookService(session)
        record: ModelRecord = record_book_service.create_record(username, record_book_id, note, amount, record_type,
                                                                tags)
        mocked_user_service_instance.fetch_user.assert_called_with(username)
        mocked_record_book_repository_instance.fetch_record_book.assert_called_with(record_book_id,
                                                                                    mock_model_user().id)
        mocked_record_repository_instance.save.assert_called_once()
        mocked_record_book_repository_instance.update_net_balance_and_tags.assert_called_once()

    assert isinstance(record, ModelRecord)


@patch('src.service.record_book.UserService')
@patch('src.service.record_book.RecordBookRepository')
@patch('src.service.record_book.RecordRepository')
def test_should_raise_record_book_not_found_exception_given_invalid_record_book_id(mocked_record_repository,
                                                                                   mocked_record_book_repository,
                                                                                   mocked_user_service):
    record_book_id = mock_model_record_book().id
    username = mock_model_user().username
    note = "Sample Expense Record"
    amount = 20.92
    record_type = RecordType.EXPENSE
    tags = ["test_tag_1"]

    mocked_user_service_instance = MagicMock(spec=UserRepository)
    mocked_user_service_instance.fetch_user.return_value = mock_model_user()
    mocked_user_service.return_value = mocked_user_service_instance

    mocked_record_book_repository_instance = MagicMock(spec=RecordBookRepository)
    mocked_record_book_repository_instance.fetch_record_book.return_value = None
    mocked_record_book_repository.return_value = mocked_record_book_repository_instance

    mocked_record_repository_instance = MagicMock(spec=RecordRepository)
    mocked_record_repository.return_value = mocked_record_repository_instance

    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        record_book_service = RecordBookService(session)
        with pytest.raises(RecordBookNotFoundException):
            record_book_service.create_record(username, record_book_id, note, amount, record_type,
                                              tags)
        mocked_user_service_instance.fetch_user.assert_called_with(username)


@patch('src.service.record_book.UserService')
@patch('src.service.record_book.RecordBookRepository')
def test_should_fetch_record_book_given_record_id_and_user(mocked_record_book_repository, mocked_user_service):
    record_book_id = str(uuid.uuid4())
    username = "test_username"
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    mocked_user_service_instance = MagicMock(spec=UserRepository)
    mocked_user_service_instance.fetch_user.return_value = mock_model_user()
    mocked_user_service.return_value = mocked_user_service_instance

    mocked_record_book_repository_instance = MagicMock(spec=RecordBookRepository)
    mocked_record_book_repository_instance.fetch_record_book.return_value = MagicMock(spec=tables.RecordBook)
    mocked_record_book_repository.return_value = mocked_record_book_repository_instance

    with mocked_session_class(mocked_engine) as session:
        record_book_service = RecordBookService(session)
        record_book: ModelRecordBook = record_book_service.fetch_record_book(record_book_id, username)
        mocked_user_service_instance.fetch_user.assert_called_with(username)
        mocked_record_book_repository_instance.fetch_record_book.assert_called_once_with(record_book_id,
                                                                                         mock_model_user().id)

    assert isinstance(record_book, ModelRecordBook)


@patch('src.service.record_book.UserService')
@patch('src.service.record_book.RecordBookRepository')
def test_should_raise_user_not_found_exception_given_invalid_user(mocked_record_book_repository, mocked_user_service):
    record_book_id = str(uuid.uuid4())
    username = "test_username"
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    mocked_user_service_instance = MagicMock(spec=UserRepository)
    mocked_user_service_instance.fetch_user.return_value = None
    mocked_user_service.return_value = mocked_user_service_instance

    mocked_record_book_repository_instance = MagicMock(spec=RecordBookRepository)
    mocked_record_book_repository_instance.fetch_record_book.return_value = MagicMock(spec=tables.RecordBook)
    mocked_record_book_repository.return_value = mocked_record_book_repository_instance

    with mocked_session_class(mocked_engine) as session:
        record_book_service = RecordBookService(session)
        with pytest.raises(UserNotFoundException):
            record_book_service.fetch_record_book(record_book_id, username)
        mocked_user_service_instance.fetch_user.assert_called_with(username)


@patch('src.service.record_book.UserService')
@patch('src.service.record_book.RecordBookRepository')
def test_should_fetch_record_books_given_username(mocked_record_book_repository, mocked_user_service):
    username = "test_username"
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    mocked_user_service_instance = MagicMock(spec=UserRepository)
    mocked_user_service_instance.fetch_user.return_value = mock_model_user()
    mocked_user_service.return_value = mocked_user_service_instance

    mocked_record_book_repository_instance = MagicMock(spec=RecordBookRepository)
    mocked_record_book_repository_instance.fetch_record_books.return_value = [MagicMock(spec=tables.RecordBook),
                                                                              MagicMock(spec=tables.RecordBook)]
    mocked_record_book_repository.return_value = mocked_record_book_repository_instance

    with mocked_session_class(mocked_engine) as session:
        record_book_service = RecordBookService(session)
        record_books: List[ModelRecordBook] = record_book_service.fetch_record_books(username)
        mocked_user_service_instance.fetch_user.assert_called_with(username)
        mocked_record_book_repository_instance.fetch_record_books.assert_called_once_with(mock_model_user().id)

    assert isinstance(record_books, List)
    assert len(record_books) == 2
    assert isinstance(record_books[0], ModelRecordBook)
