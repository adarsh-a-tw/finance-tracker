from sqlalchemy import select
from sqlalchemy.orm import Session

from tables import RecordBook


class RecordBookRepository:  # pylint: disable=too-few-public-methods
    def __init__(self, db_session):
        self._session: Session = db_session

    def save(self, record_book: RecordBook):
        self._session.add(record_book)

    def fetch_record_book(self, record_book_id, user_id):
        statement = select(RecordBook).filter_by(id=record_book_id).filter_by(user_id=user_id)
        data_record_book = self._session.scalars(statement=statement).one_or_none()
        return data_record_book

    def update_record_book(self, record_book: RecordBook):
        self._session.merge(record_book)

    def fetch_record_books(self, user_id):
        statement = select(RecordBook).filter_by(user_id=user_id)
        data_record_books = self._session.scalars(statement=statement).all()
        return data_record_books
