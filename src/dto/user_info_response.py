from pydantic import BaseModel


class UserInfoResponse(BaseModel):
    id: str
    username: str
    email: str
