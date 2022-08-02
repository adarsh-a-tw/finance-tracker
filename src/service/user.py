from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy import select

from config.secrets import get_secret
from src.model.user import User as ModelUser
from tables import User
import jwt


class UserService:
    def __init__(self, db_session):
        self._session = db_session

    def authenticate(self, username, password):
        user: ModelUser = self.fetch_user(username)
        if user.check_password(password):
            return self._generate_jwt(user)

    def fetch_user(self, username) -> Optional[ModelUser]:
        statement = select(User).filter_by(username=username)
        model_user = None
        db_user: User = self._session.scalars(statement=statement).one_or_none()
        if db_user:
            model_user = ModelUser.from_data_model(db_user)
        return model_user

    def _generate_jwt(self, user: ModelUser) -> str:
        return jwt.encode({'username': user.username, 'id': user.id, 'email': user.email,
                           'exp': timedelta(hours=1) + datetime.now()}, key=get_secret("SECRET_KEY"))
