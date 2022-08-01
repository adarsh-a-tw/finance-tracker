from __future__ import annotations

from datetime import datetime
import uuid
from dataclasses import dataclass, field
from typing import Union, List

from src.records.domain.record_type import RecordType
from src.records.exceptions import TagNotFoundException


@dataclass
class Record:
    record: uuid.UUID
    note: str
    amount: float
    type: RecordType = RecordType.EXPENSE
    added_at: datetime = datetime.now()
    tags: set = field(default_factory=set)

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
