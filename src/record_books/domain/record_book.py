import uuid
from dataclasses import dataclass, field

from currencies.domain.currency import Currency
from currencies.domain.currency_type import CurrencyType
from currencies.services.coinbase_service import fetch_data_from_coinbase
from records.domain.record import Record
from records.domain.record_type import RecordType
from users.domain.user import User


@dataclass
class RecordBook:
    record_id: uuid.UUID
    name: str
    user: User
    default_currency_type: CurrencyType = CurrencyType.RUPEE
    _records: dict = field(default_factory=dict)
    _net_balance: Currency = Currency(0, default_currency_type)
    _currency_conversion_api = fetch_data_from_coinbase

    def __init__(self, record_id, name, user, default_currency_type=CurrencyType.RUPEE,
                 _records=None,
                 _net_balance=Currency(0, default_currency_type),
                 _currency_conversion_api=fetch_data_from_coinbase):
        if _records is None:
            _records = {}
        self.record_id = record_id
        self.name = name
        self.user = user
        self.default_currency_type = default_currency_type
        self._records = _records
        self._net_balance = _net_balance
        self._currency_conversion_api = _currency_conversion_api

    def add(self, note, amount, record_type: RecordType):
        record_id = uuid.uuid4()
        record = Record(record_id, note, amount, record_type)
        self._records[record_id] = record
        self._update_balance(record)
        return record_id

    def get(self, record_id):
        return self._records.get(record_id)

    def net_balance(self):
        return self._net_balance

    def _update_balance(self, record: Record):
        if record.type == RecordType.EXPENSE:
            self._net_balance = self._net_balance.sub(
                record.amount, conversion_api=self._currency_conversion_api
            )
        else:
            self._net_balance = self._net_balance.add(
                record.amount, conversion_api=self._currency_conversion_api
            )
