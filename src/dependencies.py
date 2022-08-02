from src.config.db import DB


def get_session():
    session = DB.get_session()
    yield session


def mock_get_session():
    session = DB.get_test_session()
    yield session
