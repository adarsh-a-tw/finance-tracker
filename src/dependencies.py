from typing import Optional

import jwt
from fastapi import Header

from config.secrets import get_secret
from src.exceptions import InvalidAuthTokenException
from src.config.db import DB


def get_session():
    session = DB.get_session()
    yield session


def mock_get_session():
    session = DB.get_test_session()
    yield session


def verify_auth(x_api_token: Optional[str] = Header(None)) -> dict:
    if not x_api_token:
        raise InvalidAuthTokenException
    try:
        user_info = jwt.decode(x_api_token, get_secret('SECRET_KEY'), algorithms=["HS256"])
        user_info.pop('exp')
        return user_info
    except Exception:
        raise InvalidAuthTokenException
