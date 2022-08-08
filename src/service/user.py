import uuid
from datetime import timedelta, datetime
from typing import Optional

import jwt

from config.secrets import get_secret
from src.exceptions import InvalidCredentialsException, UsernameAlreadyExistsException, EmailAlreadyExistsException
from src.model.user import User as ModelUser
from src.repository.user import UserRepository


class UserService:
    def __init__(self, db_session):
        self.repository: UserRepository = UserRepository(db_session=db_session)

    def authenticate(self, username, password):
        user: ModelUser = self.fetch_user(username)
        if user and user.check_password(password):
            return self._generate_jwt(user)
        raise InvalidCredentialsException()

    def fetch_user(self, username) -> Optional[ModelUser]:
        db_user = self.repository.fetch_user(username)
        return ModelUser.from_data_model(db_user) if db_user else None

    @staticmethod
    def _generate_jwt(user: ModelUser) -> str:
        return jwt.encode({'username': user.username, 'id': user.id, 'email': user.email,
                           'exp': timedelta(hours=1) + datetime.now()}, key=get_secret("SECRET_KEY"))

    def save_user(self, user: ModelUser):
        data_user = user.data_model()
        self.repository.save(data_user)

    def create_user(self, username, email, password):
        if self.repository.fetch_user(username):
            raise UsernameAlreadyExistsException

        if self.repository.fetch_user_by_email(email):
            raise EmailAlreadyExistsException

        model_user = ModelUser(id=str(uuid.uuid4()), username=username, email=email)
        model_user.set_password(password)

        self.save_user(model_user)
