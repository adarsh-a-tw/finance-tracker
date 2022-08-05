import datetime
from typing import List

from pydantic import BaseModel

from src.model.record_type import RecordType


class CreateRecordResponse(BaseModel):
    id: str
    note: str
    amount: float
    type: RecordType
    added_at: datetime.datetime
    tags: List[str]
