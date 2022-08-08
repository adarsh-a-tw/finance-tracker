from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from tables import User


class UserRepository:
    def __init__(self, db_session):
        self._session: Session = db_session

    def fetch_user(self, username) -> Optional[User]:
        statement = select(User).filter_by(username=username)
        return self._session.scalars(statement=statement).one_or_none()

    def save(self, user: User):
        self._session.add(user)

    def fetch_user_by_email(self, email):
        statement = select(User).filter_by(email=email)
        return self._session.scalars(statement=statement).one_or_none()
