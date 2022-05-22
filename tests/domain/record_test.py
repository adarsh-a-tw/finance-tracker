import uuid

from currencies.domain.currency import Currency
from currencies.domain.currency_type import CurrencyType
from records.domain.record import Record
from records.domain.record_type import RecordType


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
