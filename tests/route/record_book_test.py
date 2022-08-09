# pylint: disable=redefined-outer-name
import uuid

import pytest

from src.model.record_book import RecordBook
from src.model.record_type import RecordType
from src.model.user import User
from src.service.record_book import RecordBookService
from src.service.user import UserService

USER_ID = str(uuid.uuid4())

USERNAME = "test_user"
PASSWORD = "test_password"

user = User(id=USER_ID, username=USERNAME, email="test_user@domain.com")
user.set_password(PASSWORD)


def get_auth_token(client):
    response = client.post("/users/authenticate", json={"username": USERNAME, "password": PASSWORD})
    return response.json()['token']


@pytest.fixture(autouse=True)
def setup_user(get_test_session):
    with get_test_session.begin() as session:
        user_service = UserService(session)
        user_service.save_user(user)


@pytest.fixture
def default_record_book(get_test_session):
    with get_test_session.begin() as session:
        record_book_service = RecordBookService(session)
        record_book = record_book_service.create_record_book("test_record_book", USERNAME)
        record_book_service.create_record(username=user.username, record_book_id=record_book.id,
                                          note="Test Expense", amount=10, record_type=RecordType.EXPENSE,
                                          tags=['test'])
        return record_book_service.fetch_record_book(record_book_id=record_book.id, username=USERNAME)


def test_should_create_record_book(client):
    record_book_details = {'name': 'Test book'}

    response = client.post("/record_books", json=record_book_details, headers={'x-api-token': get_auth_token(client)})

    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'Test book'


def test_should_create_record(client, default_record_book):
    record_details = {'note': 'test_expense', 'amount': 10.0, 'type': 'EXPENSE', 'tags': ['test_tag']}

    response = client.post(f"/record_books/{default_record_book.id}/records", json=record_details,
                           headers={'x-api-token': get_auth_token(client)})

    data = response.json()
    assert response.status_code == 201
    assert data['note'] == 'test_expense'
    assert data['amount'] == 10.0
    assert data['type'] == 'EXPENSE'
    assert data['tags'] == ['test_tag']


def test_should_fetch_record_books_for_user(client, default_record_book):
    response = client.get("/record_books", headers={'x-api-token': get_auth_token(client)})

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["name"] == "test_record_book"
    assert data[0]["id"] == default_record_book.id
    assert data[0]["tags"] == ['test']


def test_should_fetch_record_book_with_records_for_user_given_user_id(client, default_record_book):
    response = client.get(f"/record_books/{default_record_book.id}", headers={'x-api-token': get_auth_token(client)})

    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "test_record_book"
    assert data["id"] == default_record_book.id
    assert data["tags"] == ['test']
    assert len(data["records"]) == 1


def test_should_delete_record_given_record_book_id_and_record_id(client, default_record_book: RecordBook):
    response = client.delete(f"/record_books/{default_record_book.id}/records/{default_record_book.records()[0].id}",
                             headers={'x-api-token': get_auth_token(client)})

    assert response.status_code == 204
