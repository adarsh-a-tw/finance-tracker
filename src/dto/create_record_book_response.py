from pydantic import BaseModel

from src.dto.user_info_response import UserInfoResponse


class CreateRecordBookResponse(BaseModel):
    id: str
    name: str
    user: UserInfoResponse
