from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from dto.authenticate_request import AuthenticateRequest
from dependencies import get_session
from src.exceptions import InvalidCredentialsException
from src.service.user import UserService

router = APIRouter()


@router.post("/authenticate")
def authenticate(request_body: AuthenticateRequest, session_class: Session = Depends(get_session)):
    username, password = request_body.username, request_body.password
    with session_class.begin() as session:
        service = UserService(session)
        token = service.authenticate(username, password)

    return {
        "token": token
        }

