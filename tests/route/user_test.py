import uuid

import pytest

from src.model.user import User
from src.service.user import UserService

USER_ID = str(uuid.uuid4())


@pytest.fixture(autouse=True)
def setup_default_user(get_test_session):
    with get_test_session.begin() as session:
        user = User(id=USER_ID, username="test_user", email="test_user@domain.com")
        user.set_password("test_password")
        user_service = UserService(session)
        user_service.save_user(user)


def test_authenticate_success(client):
    response = client.post("/users/authenticate", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    assert 'token' in response.json()


def test_authenticate_failure_invalid_username(client):
    response = client.post("/users/authenticate",
                           json={"username": "test_invalid_user", "password": "test_password"})
    assert response.status_code == 401


def test_get_user_information(client):
    auth_response = client.post("/users/authenticate", json={"username": "test_user", "password": "test_password"})
    auth_token = auth_response.json()['token']
    response = client.get("/users/me", headers={'x-api-token': auth_token})
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == "test_user"
    assert data['email'] == "test_user@domain.com"
    assert data['id'] == USER_ID
