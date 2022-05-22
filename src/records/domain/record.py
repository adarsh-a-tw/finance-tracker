from datetime import datetime
import uuid
from dataclasses import dataclass

from currencies.domain.currency import Currency
from records.domain.record_type import RecordType


@dataclass
class Record:
    record_id: uuid.UUID
    note: str
    amount: Currency
    type: RecordType = RecordType.EXPENSE
    added_at: datetime = datetime.now()
