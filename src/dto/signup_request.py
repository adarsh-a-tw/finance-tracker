import re

from pydantic import BaseModel, root_validator

from src.exceptions import PasswordsDontMatchException, EmailInvalidException


def is_email_valid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


class SignupRequest(BaseModel):
    username: str
    password: str
    confirm_password: str
    email: str

    @root_validator
    def validate_fields(cls, values):  # pylint: disable=no-self-argument,no-self-use
        pw1, pw2 = values.get('password'), values.get('confirm_password')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise PasswordsDontMatchException

        email = values.get("email")
        if not is_email_valid(email):
            raise EmailInvalidException

        return values
