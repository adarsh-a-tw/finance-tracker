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
    assert 'refresh_token' in response.json()


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


def test_user_signup(client):
    user_information = {"username": "new_user", "password": "new_password", "confirm_password": "new_password",
                        "email": "new_email@domain.com"}
    response = client.post("/users/signup", json=user_information)
    assert response.status_code == 201


def test_user_signup_failure_when_username_not_unique(client):
    user_information = {"username": "test_user", "password": "new_password", "confirm_password": "new_password",
                        "email": "new_email@domain.com"}
    response = client.post("/users/signup", json=user_information)
    assert response.status_code == 400
    assert response.json()['message'] == 'Username already exists.'


def test_user_signup_failure_when_email_not_unique(client):
    user_information = {"username": "new_user", "password": "new_password", "confirm_password": "new_password",
                        "email": "test_user@domain.com"}
    response = client.post("/users/signup", json=user_information)
    assert response.status_code == 400
    assert response.json()['message'] == 'Email already exists.'


def test_user_signup_failure_when_email_not_valid(client):
    user_information = {"username": "new_user", "password": "new_password", "confirm_password": "new_password",
                        "email": "test_user"}
    response = client.post("/users/signup", json=user_information)
    assert response.status_code == 400
    assert response.json()['message'] == 'Email is invalid.'


def test_user_signup_failure_when_passwords_dont_match(client):
    user_information = {"username": "new_user", "password": "new_password", "confirm_password": "new_password2",
                        "email": "new_user@domain.com"}
    response = client.post("/users/signup", json=user_information)
    assert response.status_code == 400
    assert response.json()['message'] == 'Passwords dont match.'


def test_authenticate_using_refresh_token(client):
    auth_response = client.post("/users/authenticate", json={"username": "test_user", "password": "test_password"})
    refresh_token = auth_response.json()['refresh_token']
    response = client.post("/users/refresh_token", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert data['token'] is not None
    assert data['refresh_token'] is not None
