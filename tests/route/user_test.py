import unittest
import uuid

from fastapi.testclient import TestClient

import tables
from config.db import DB
from dependencies import get_session, mock_get_session
from main import app
from src.model.user import User
from src.service.user import UserService

app.dependency_overrides[get_session] = mock_get_session

client = TestClient(app)

user_id = str(uuid.uuid4())


class TestUserRouter(unittest.TestCase):

    def get_session(self):
        engine = DB.get_test_engine()
        base_class = DB.get_base()

        base_class.metadata.create_all(bind=engine)

        Session = DB.get_test_session()
        return Session

    def setUp(self) -> None:
        with self.get_session().begin() as session:
            user = User(id=user_id, username = "test_user", email = "test_user@domain.com")
            user.set_password("test_password")
            user_service = UserService(session)
            user_service.save_user(user)

    def tearDown(self) -> None:
        with self.get_session().begin() as session:
            session.query(tables.User).delete()

    def test_authenticate_success(self):
        response = client.post("/users/authenticate", json={"username": "test_user", "password": "test_password"})
        assert response.status_code == 200
        assert 'token' in response.json()

    def test_authenticate_failure_invalid_username(self):
        response = client.post("/users/authenticate",
                               json={"username": "test_invalid_user", "password": "test_password"})
        assert response.status_code == 401

    def test_get_user_information(self):
        auth_response = client.post("/users/authenticate", json={"username": "test_user", "password": "test_password"})
        auth_token = auth_response.json()['token']
        response = client.get("/users/me", headers={'x-api-token': auth_token})
        assert response.status_code == 200
        data = response.json()
        assert data['username'] == "test_user"
        assert data['email'] == "test_user@domain.com"
        assert data['id'] == user_id
