import uuid

from record_books.domain.record_book import RecordBook
from records.domain.record import Record
from records.domain.record_type import RecordType
from users.domain.user import User


def test_create_record_book_for_user():
    user = User(uuid.uuid4(), "test_username", "user_email@domain.com")

    record_book = RecordBook(uuid.uuid4(), "Test Book", user)

    assert record_book.user is user


def test_create_expense_in_record_book():
    user = User(uuid.uuid4(), "test_username", "user_email@domain.com")
    record_book = RecordBook(uuid.uuid4(), "Test Book", user)
    note = "Test Expense"
    amount = 10

    record_id = record_book.add(note, amount, RecordType.EXPENSE)

    record: Record = record_book._records.get(record_id)  # pylint: disable=W0212
    assert record.type == RecordType.EXPENSE
    assert record.amount == amount
    assert record.note == note
    assert record_book.net_balance() == -10


def test_fetch_expense_in_record_book():
    user = User(uuid.uuid4(), "test_username", "user_email@domain.com")
    record_book = RecordBook(uuid.uuid4(), "Test Book", user)
    note = "Test Expense"
    amount = 10
    record_id = record_book.add(note, amount, RecordType.EXPENSE)

    record: Record = record_book.get(record_id)

    assert record.type == RecordType.EXPENSE
    assert record.amount == amount
    assert record.note == note


def test_net_balance_of_record_book():
    user = User(uuid.uuid4(), "test_username", "user_email@domain.com")
    record_book = RecordBook(uuid.uuid4(), "Test Book", user)
    ten_rupees = 10
    twenty_rupees = 20
    record_book.add("Test Income", twenty_rupees, RecordType.INCOME)
    record_book.add("Test Expense", ten_rupees, RecordType.EXPENSE)

    balance: float = record_book.net_balance()

    assert balance == ten_rupees


def test_fetch_all_tags_of_records_in_record_book():
    user = User(uuid.uuid4(), "test_username", "user_email@domain.com")
    record_book = RecordBook(uuid.uuid4(), "Test Book", user)
    ten_rupees = 10
    twenty_rupees = 20
    tag_list_1 = ["test_tag_1", "test_tag_2"]
    tag_list_2 = ["test_tag_3", "test_tag_4", "test_tag_5"]
    record_book.add("Test Income", twenty_rupees, RecordType.INCOME, tags=tag_list_1)
    record_book.add("Test Expense", ten_rupees, RecordType.EXPENSE, tags=tag_list_2)

    tags: set = record_book.tags()

    assert tags == {*tag_list_1, *tag_list_2}
