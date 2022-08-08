from typing import List
from pydantic import BaseModel

from src.dto.record_info_response import RecordInfoResponse


class RecordBookInfoResponse(BaseModel):
    id: str
    name: str
    net_balance: float
    tags: set
    records: List[RecordInfoResponse]
