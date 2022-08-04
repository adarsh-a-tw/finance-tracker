import uuid

from src.model.user import User
from src.service.user import UserService

USER_ID = str(uuid.uuid4())

USERNAME = "test_user"
PASSWORD = "test_password"


def get_auth_token(client):
    response = client.post("/users/authenticate", json={"username": USERNAME, "password": PASSWORD})
    return response.json()['token']


def test_should_create_record_book(client, get_test_session):
    user = User(id=USER_ID, username=USERNAME, email="test_user@domain.com")
    user.set_password(PASSWORD)
    with get_test_session.begin() as session:
        user_service = UserService(session)
        user_service.save_user(user)
    record_book_details = {'name': 'Test book'}

    response = client.post("/record_books", json=record_book_details, headers={'x-api-token': get_auth_token(client)})

    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'Test book'
