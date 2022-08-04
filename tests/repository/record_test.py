from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from mocks.record import mock_data_record
from src.repository.record import RecordRepository


def test_should_save_record():
    table_record = mock_data_record()
    mocked_session_class = MagicMock(spec=Session)
    mocked_engine = MagicMock()

    with mocked_session_class(mocked_engine) as session:
        repository: RecordRepository = RecordRepository(db_session=session)
        repository.save(table_record)
        session.add.assert_called_once_with(table_record)
