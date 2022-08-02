import uuid
from dataclasses import dataclass, field
from typing import List

from src.model.record import Record
from src.model.record_type import RecordType
from src.model.user import User


@dataclass
class RecordBook:  # pylint: disable=invalid-name
    id: uuid.UUID
    name: str
    user: User
    _records: dict = field(default_factory=dict)
    _net_balance: float = 0
    _tags: set = field(default_factory=set)

    def __init__(self, record_id, name, user, _net_balance=0):
        self.record_book_id = record_id
        self.name = name
        self.user = user
        self._records = {}
        self._net_balance = _net_balance
        self._tags = set()

    def add(self, note: str, amount: float, record_type: RecordType, tags=None):
        record_id = uuid.uuid4()
        record = Record(record_id, note, amount, record_type)
        if tags:
            record.tag(tags, bulk=True)
            self._update_tags(tags)
        self._records[record_id] = record
        self._update_balance(record)
        return record_id

    def get(self, record_id):
        return self._records.get(record_id)

    def net_balance(self):
        return self._net_balance

    def _update_balance(self, record: Record):
        if record.type == RecordType.EXPENSE:
            self._net_balance -= record.amount
        else:
            self._net_balance += record.amount

    def tags(self):
        return self._tags

    def _update_tags(self, tags: List):
        self._tags = self._tags.union(set(tags))
