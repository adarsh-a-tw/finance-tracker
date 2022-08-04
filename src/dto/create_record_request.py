from typing import List

from pydantic import BaseModel

from src.model.record_type import RecordType


class CreateRecordRequest(BaseModel):
    note: str
    amount: float
    type: RecordType
    tags: List[str]
