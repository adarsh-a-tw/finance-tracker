from sqlalchemy.orm import Session

from tables import Record


class RecordRepository:  # pylint: disable=too-few-public-methods
    def __init__(self, db_session):
        self._session: Session = db_session

    def save(self, record: Record):
        self._session.add(record)
