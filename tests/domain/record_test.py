import uuid

import pytest

from currencies.domain.currency import Currency
from currencies.domain.currency_type import CurrencyType
from records.domain.record import Record
from records.domain.record_type import RecordType
from records.exceptions import TagNotFoundException


def test_create_income_record():
    value = 10.00
    currency = Currency(value, CurrencyType.RUPEE)
    note = "Sample Income"
    record_id = uuid.uuid4()

    record = Record(record_id, note, currency, RecordType.INCOME)

    assert record.type == RecordType.INCOME


def test_create_expense_record():
    value = 10.00
    currency = Currency(value, CurrencyType.RUPEE)
    note = "Sample Expense"
    record_id = uuid.uuid4()

    record = Record(record_id, note, currency, RecordType.EXPENSE)

    assert record.type == RecordType.EXPENSE


def test_create_record_with_tags():
    value = 10.00
    currency = Currency(value, CurrencyType.RUPEE)
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name = "test"
    record = Record(record_id, note, currency, RecordType.EXPENSE)

    record.tag(tag_name)

    assert tag_name in record.tags


def test_untag_tag_from_record():
    value = 10.00
    currency = Currency(value, CurrencyType.RUPEE)
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name = "test"
    record = Record(record_id, note, currency, RecordType.EXPENSE)
    record.tag(tag_name)

    record.untag(tag_name)

    assert tag_name not in record.tags


def test_create_record_with_multiple_tags_in_bulk():
    value = 10.00
    currency = Currency(value, CurrencyType.RUPEE)
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name_1 = "test1"
    tag_name_2 = "test2"
    record = Record(record_id, note, currency, RecordType.EXPENSE)

    record.tag([tag_name_1, tag_name_2], bulk=True)

    assert tag_name_1 in record.tags
    assert tag_name_2 in record.tags


def test_should_not_untag_non_existing_tag_from_record():
    value = 10.00
    currency = Currency(value, CurrencyType.RUPEE)
    note = "Sample Expense"
    record_id = uuid.uuid4()
    tag_name = "test"
    record = Record(record_id, note, currency, RecordType.EXPENSE)

    with pytest.raises(TagNotFoundException):
        record.untag(tag_name)
