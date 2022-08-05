from pydantic import BaseModel


class RecordBookListViewResponse(BaseModel):
    id: str
    name: str
    net_balance: float
    tags: set
