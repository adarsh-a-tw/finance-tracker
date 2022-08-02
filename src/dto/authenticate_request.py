from pydantic import BaseModel


class AuthenticateRequest(BaseModel):
    username: str
    password: str
