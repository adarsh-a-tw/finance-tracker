from __future__ import annotations

from datetime import datetime
import uuid
from dataclasses import dataclass, field
from typing import Union, List, Set

import tables
from src.model.record_type import RecordType
from src.exceptions import TagNotFoundException


@dataclass
class Record:  # pylint: disable=invalid-name
    id: str
    note: str
    amount: float
    type: RecordType = RecordType.EXPENSE
    added_at: datetime = datetime.now()
    tags: Set[str] = field(default_factory=set)

    def tag(self, tag_name: Union[str | List[str]], bulk=False):
        if bulk:
            for tag in tag_name:
                self.tags.add(tag)
        else:
            self.tags.add(tag_name)

    def untag(self, tag_name):
        if tag_name not in self.tags:
            raise TagNotFoundException
        self.tags.remove(tag_name)

    @classmethod
    def from_data_model(cls, data_record: tables.Record) -> 'Record':
        return cls(id=data_record.id, note=data_record.note, amount=data_record.amount,
                   type=RecordType(data_record.type), added_at=data_record.added_at)

    def data_model(self, record_book_id: str) -> tables.Record:
        return tables.Record(id=self.id, record_book_id=record_book_id, amount=self.amount, note=self.note,
                             type=self.type.value, added_at=self.added_at)
