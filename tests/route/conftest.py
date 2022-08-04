# pylint: disable=redefined-outer-name
import pytest
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from config.db import DB
from dependencies import get_session
from main import app


@pytest.fixture
def db_engine():
    engine = DB.get_test_engine()
    base_class = DB.get_base()

    base_class.metadata.create_all(bind=engine)
    yield engine
    base_class.metadata.drop_all(bind=engine)


@pytest.fixture
def get_test_session(db_engine):
    yield sessionmaker(bind=db_engine)


@pytest.fixture
def client(get_test_session):
    app.dependency_overrides[get_session] = lambda: get_test_session

    with TestClient(app) as test_client:
        yield test_client
