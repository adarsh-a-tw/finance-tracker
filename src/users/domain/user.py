import hashlib
import uuid
from dataclasses import dataclass


@dataclass
class User:
    id: uuid.UUID
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
