import hashlib
import uuid
from dataclasses import dataclass

from sqlalchemy.orm import Session

import tables


@dataclass
class User:  # pylint: disable=invalid-name
    id: str
    username: str
    email: str
    _password: str = None
    _salt: str = None

    def set_password(self, raw_password: str) -> None:
        self._salt = uuid.uuid4().hex
        salt_mixed_raw_password = (raw_password + self._salt).encode("utf-8")
        self._password = hashlib.sha512(salt_mixed_raw_password).hexdigest()

    def check_password(self, raw_password: str) -> bool:
        salt_mixed_raw_password = (raw_password + self._salt).encode("utf-8")
        return self._password == hashlib.sha512(salt_mixed_raw_password).hexdigest()

    def data_model(self) -> tables.User:
        return tables.User(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self._password,
            salt=self._salt
        )

    @classmethod
    def from_data_model(cls, data_user) -> 'User':
        return cls(
            id=data_user.id,
            username=data_user.username,
            email=data_user.email,
            _password=data_user.password,
            _salt=data_user.salt
        )

    def save(self, session: Session):
        session.add(self.data_model())
