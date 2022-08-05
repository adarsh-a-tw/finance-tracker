import uuid

import pytest

import tables
from src.model.record import Record
from src.model.record_type import RecordType
from src.exceptions import TagNotFoundException

record_id = str(uuid.uuid4())


def test_create_income_record():
    amount = 10.00
    note = "Sample Income"

    record = Record(record_id, note, amount, RecordType.INCOME)

    assert record.id == record_id
    assert record.note == note
    assert record.amount == amount
    assert record.type == RecordType.INCOME


def test_create_expense_record():
    amount = 10.00
    note = "Sample Expense"

    record = Record(record_id, note, amount, RecordType.EXPENSE)

    assert record.id == record_id
    assert record.note == note
    assert record.amount == amount
    assert record.type == RecordType.EXPENSE


def test_create_record_with_tags():
    amount = 10.00
    note = "Sample Expense"
    tag_name = "test"
    record = Record(record_id, note, amount, RecordType.EXPENSE)

    record.tag(tag_name)

    assert tag_name in record.tags


def test_untag_tag_from_record():
    amount = 10.00
    note = "Sample Expense"
    tag_name = "test"
    record = Record(record_id, note, amount, RecordType.EXPENSE)
    record.tag(tag_name)

    record.untag(tag_name)

    assert tag_name not in record.tags


def test_create_record_with_multiple_tags_in_bulk():
    amount = 10.00
    note = "Sample Expense"
    tag_name_1 = "test1"
    tag_name_2 = "test2"
    record = Record(record_id, note, amount, RecordType.EXPENSE)

    record.tag([tag_name_1, tag_name_2], bulk=True)

    assert tag_name_1 in record.tags
    assert tag_name_2 in record.tags


def test_should_not_untag_non_existing_tag_from_record():
    amount = 10.00
    note = "Sample Expense"
    tag_name = "test"
    record = Record(record_id, note, amount, RecordType.EXPENSE)

    with pytest.raises(TagNotFoundException):
        record.untag(tag_name)


def test_should_map_model_record_to_data_model():
    amount = 10.00
    note = "Sample Expense"
    model_record = Record(record_id, note, amount, RecordType.EXPENSE)

    data_record: tables.Record = model_record.data_model(str(uuid.uuid4()))

    assert data_record.id == model_record.id
    assert data_record.note == model_record.note
    assert data_record.amount == model_record.amount
    assert data_record.type == RecordType.EXPENSE.value


def test_should_create_model_record_from_data_model():
    amount = 10.00
    note = "Sample Expense"
    data_record = tables.Record(id=record_id, note=note, amount=amount, type=RecordType.EXPENSE.value,
                                record_book_id=str(uuid.uuid4()))

    model_record: Record = Record.from_data_model(data_record)

    assert data_record.id == model_record.id
    assert data_record.note == model_record.note
    assert data_record.amount == model_record.amount
    assert model_record.type == RecordType.EXPENSE


def test_should_map_model_record_to_data_model_with_tags():
    amount = 10.00
    note = "Sample Expense"
    model_record = Record(record_id, note, amount, RecordType.EXPENSE, tags={'test_tag'})

    data_record: tables.Record = model_record.data_model(str(uuid.uuid4()))

    tags = [row.tag for row in data_record.tag_map]

    assert data_record.id == model_record.id
    assert data_record.note == model_record.note
    assert data_record.amount == model_record.amount
    assert data_record.type == RecordType.EXPENSE.value
    assert set(tags) == model_record.tags


def test_should_create_model_record_from_data_model_with_tags():
    amount = 10.00
    note = "Sample Expense"
    data_tags = [tables.RecordTagMapping(record_id=record_id, tag=str(i)) for i in range(10)]
    data_record = tables.Record(id=record_id, note=note, amount=amount, type=RecordType.EXPENSE.value,
                                record_book_id=str(uuid.uuid4()), tag_map=data_tags)

    model_record: Record = Record.from_data_model(data_record)

    tags = [row.tag for row in data_record.tag_map]
    assert data_record.id == model_record.id
    assert data_record.note == model_record.note
    assert data_record.amount == model_record.amount
    assert model_record.type == RecordType.EXPENSE
    assert model_record.tags == set(tags)
