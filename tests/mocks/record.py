import datetime
import uuid

import tables
from src.model.record_type import RecordType
from src.model.record import Record as ModelRecord

RECORD_ID = str(uuid.uuid4())
AMOUNT = 10.00
NOTE = "Sample Expense"
ADDED_AT = datetime.datetime.now()


def mock_data_record():
    return tables.Record(id=RECORD_ID, note=NOTE, amount=AMOUNT, type=RecordType.EXPENSE.value,
                         record_book_id=str(uuid.uuid4()), added_at=ADDED_AT)


def mock_model_record():
    return ModelRecord(id=RECORD_ID, note=NOTE, amount=AMOUNT, type=RecordType.EXPENSE,
                       added_at=ADDED_AT)
