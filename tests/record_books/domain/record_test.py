import uuid

import pytest

from src.record_books.domain.record import Record
from src.record_books.domain.record_type import RecordType
from src.record_books.exceptions import TagNotFoundException


def test_create_income_record():
    amount = 10.00
    note = "Sample Income"
    record_id = uuid.uuid4()

    record = Record(record_id, note, amount, RecordType.INCOME)

    assert record.id == record_id
    assert record.note == note
    assert record.amount == amount
    assert record.type == RecordType.INCOME


def test_create_expense_record():
    amount = 10.00
    note = "Sample Expense"
    record_id = uuid.uuid4()

    record = Record(record_id, note, amount, RecordType.EXPENSE)

    assert record.id == record_id
    assert record.note == note
    assert record.amount == amount
    assert record.type == RecordType.EXPENSE


def test_create_record_with_tags():
    amount = 10.00
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name = "test"
    record = Record(record_id, note, amount, RecordType.EXPENSE)

    record.tag(tag_name)

    assert tag_name in record.tags


def test_untag_tag_from_record():
    amount = 10.00
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name = "test"
    record = Record(record_id, note, amount, RecordType.EXPENSE)
    record.tag(tag_name)

    record.untag(tag_name)

    assert tag_name not in record.tags


def test_create_record_with_multiple_tags_in_bulk():
    amount = 10.00
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name_1 = "test1"
    tag_name_2 = "test2"
    record = Record(record_id, note, amount, RecordType.EXPENSE)

    record.tag([tag_name_1, tag_name_2], bulk=True)

    assert tag_name_1 in record.tags
    assert tag_name_2 in record.tags


def test_should_not_untag_non_existing_tag_from_record():
    amount = 10.00
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name = "test"
    record = Record(record_id, note, amount, RecordType.EXPENSE)

    with pytest.raises(TagNotFoundException):
        record.untag(tag_name)
