from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from dependencies import get_session, verify_auth
from dto.authenticate_request import AuthenticateRequest
from dto.signup_request import SignupRequest
from src.service.user import UserService

router = APIRouter()


@router.post("/authenticate")
def authenticate(request_body: AuthenticateRequest, session_class: Session = Depends(get_session)):
    username, password = request_body.username, request_body.password
    with session_class.begin() as session:
        service = UserService(session)
        token, refresh_token = service.authenticate(username, password)

    return {
        "token": token,
        "refresh_token": refresh_token
    }


@router.post("/refresh_token")
def refresh_token_pair(request_body: dict = Body(), session_class: Session = Depends(get_session)):
    refresh_token = request_body['refresh_token']
    with session_class.begin() as session:
        service = UserService(session)
        token, refresh_token = service.get_token_pair(refresh_token)

    return {
        "token": token,
        "refresh_token": refresh_token
    }


@router.get("/me")
def get_user_info(user_info: dict = Depends(verify_auth)):
    return user_info


@router.post("/signup", status_code=201)
def signup(request_body: SignupRequest, session_class: Session = Depends(get_session)):
    username, password, email = request_body.username, request_body.password, request_body.email
    with session_class.begin() as session:
        service = UserService(session)
        service.create_user(username, email, password)
