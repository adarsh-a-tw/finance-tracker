from sqlalchemy.orm import Session

from tables import RecordBook


class RecordBookRepository:  # pylint: disable=too-few-public-methods
    def __init__(self, db_session):
        self._session: Session = db_session

    def save(self, record_book: RecordBook):
        self._session.add(record_book)
