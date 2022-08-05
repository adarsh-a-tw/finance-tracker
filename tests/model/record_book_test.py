import datetime
import uuid

import tables
from src.model.record_book import RecordBook
from src.model.record import Record
from src.model.record_type import RecordType
from src.model.user import User


def test_create_record_book_for_user():
    user = User(str(uuid.uuid4()), "test_username", "user_email@domain.com")

    record_book = RecordBook(str(uuid.uuid4()), "Test Book", user)

    assert record_book.user is user


def test_create_expense_in_record_book():
    user = User(str(uuid.uuid4()), "test_username", "user_email@domain.com")
    record_book = RecordBook(str(uuid.uuid4()), "Test Book", user)
    note = "Test Expense"
    amount = 10

    record_id = record_book.add(note, amount, RecordType.EXPENSE)

    record: Record = record_book._records.get(record_id)  # pylint: disable=W0212
    assert record.type == RecordType.EXPENSE
    assert record.amount == amount
    assert record.note == note
    assert record_book.net_balance() == -10


def test_fetch_expense_in_record_book():
    user = User(str(uuid.uuid4()), "test_username", "user_email@domain.com")
    record_book = RecordBook(str(uuid.uuid4()), "Test Book", user)
    note = "Test Expense"
    amount = 10
    record_id = record_book.add(note, amount, RecordType.EXPENSE)

    record: Record = record_book.get(record_id)

    assert record.type == RecordType.EXPENSE
    assert record.amount == amount
    assert record.note == note


def test_net_balance_of_record_book():
    user = User(str(uuid.uuid4()), "test_username", "user_email@domain.com")
    record_book = RecordBook(str(uuid.uuid4()), "Test Book", user)
    ten_rupees = 10
    twenty_rupees = 20
    record_book.add("Test Income", twenty_rupees, RecordType.INCOME)
    record_book.add("Test Expense", ten_rupees, RecordType.EXPENSE)

    balance: float = record_book.net_balance()

    assert balance == ten_rupees


def test_fetch_all_tags_of_records_in_record_book():
    user = User(str(uuid.uuid4()), "test_username", "user_email@domain.com")
    record_book = RecordBook(str(uuid.uuid4()), "Test Book", user)
    ten_rupees = 10
    twenty_rupees = 20
    tag_list_1 = ["test_tag_1", "test_tag_2"]
    tag_list_2 = ["test_tag_3", "test_tag_4", "test_tag_5"]
    record_book.add("Test Income", twenty_rupees, RecordType.INCOME, tags=tag_list_1)
    record_book.add("Test Expense", ten_rupees, RecordType.EXPENSE, tags=tag_list_2)

    tags: set = record_book.tags()

    assert tags == {*tag_list_1, *tag_list_2}


def test_should_map_model_record_book_to_data_model():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = str(uuid.uuid4())
    record_book_id = str(uuid.uuid4())
    model_user = User(user_id, username, email)
    model_record_book = RecordBook(id=record_book_id, name="Test Book", user=model_user)

    data_record_book: tables.RecordBook = model_record_book.data_model()

    assert data_record_book.id == model_record_book.id
    assert data_record_book.name == model_record_book.name
    assert data_record_book.user_id == model_user.id


def test_should_create_model_record_book_from_data_model():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = str(uuid.uuid4())
    record_book_id = str(uuid.uuid4())
    data_user: tables.User = tables.User(id=user_id, username=username, email=email)
    data_record_book: tables.RecordBook = tables.RecordBook(id=record_book_id, name="Test Book", user=data_user)
    model_user: User = User(user_id, username, email)

    model_record_book: RecordBook = RecordBook.from_data_model(data_record_book)

    assert model_record_book.id == data_record_book.id
    assert model_record_book.user == model_user
    assert model_record_book.name == data_record_book.name


def test_should_create_model_record_book_from_data_model_with_records():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = str(uuid.uuid4())
    record_book_id = str(uuid.uuid4())
    data_user: tables.User = tables.User(id=user_id, username=username, email=email)
    amount = 10.00
    note = "Sample Expense"
    record_id = str(uuid.uuid4())
    added_at = datetime.datetime.now()
    data_record = tables.Record(id=record_id, note=note, amount=amount, type=RecordType.EXPENSE.value,
                                record_book_id=str(uuid.uuid4()), added_at=added_at)
    data_record_book: tables.RecordBook = tables.RecordBook(id=record_book_id, name="Test Book", user=data_user,
                                                            records=[data_record])
    model_user: User = User(user_id, username, email)

    model_record: Record = Record(id=record_id, note=note, amount=amount, type=RecordType.EXPENSE,
                                  added_at=added_at)

    model_record_book: RecordBook = RecordBook.from_data_model(data_record_book, with_records=True)

    assert model_record_book.id == data_record_book.id
    assert model_record_book.user == model_user
    assert model_record_book.name == data_record_book.name
    assert model_record == model_record_book._records.get(record_id)


def test_should_map_model_record_book_to_data_model_with_tags():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = str(uuid.uuid4())
    record_book_id = str(uuid.uuid4())
    model_user = User(user_id, username, email)
    model_record_book = RecordBook(id=record_book_id, name="Test Book", user=model_user)
    model_record_book._update_tags(['1', '2'])

    data_record_book: tables.RecordBook = model_record_book.data_model()

    tags = [row.tag for row in data_record_book.tag_map]

    assert data_record_book.id == model_record_book.id
    assert data_record_book.name == model_record_book.name
    assert data_record_book.user_id == model_user.id
    assert set(tags) == {'1', '2'}


def test_should_create_model_record_book_from_data_model_with_tags():
    username = "test_username"
    email = "test_email@domain.com"
    user_id = str(uuid.uuid4())
    record_book_id = str(uuid.uuid4())
    data_user: tables.User = tables.User(id=user_id, username=username, email=email)

    data_tags = [tables.RecordBookTagMapping(record_book_id=record_book_id, tag=str(i)) for i in range(10)]

    data_record_book: tables.RecordBook = tables.RecordBook(id=record_book_id, name="Test Book", user=data_user,
                                                            tag_map=data_tags)
    model_user: User = User(user_id, username, email)

    model_record_book: RecordBook = RecordBook.from_data_model(data_record_book, with_records=True)

    tags = [row.tag for row in data_record_book.tag_map]

    assert model_record_book.id == data_record_book.id
    assert model_record_book.user == model_user
    assert model_record_book.name == data_record_book.name
    assert set(tags) == model_record_book.tags()
