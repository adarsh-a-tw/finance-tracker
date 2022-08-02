from fastapi import APIRouter

from dto.authenticate_request import AuthenticateRequest

router = APIRouter()


@router.post("/users/{username}")
def authenticate(request_body: AuthenticateRequest):
    pass
