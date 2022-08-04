import datetime
import uuid

import tables
from src.model.record_type import RecordType
from src.model.record import Record as ModelRecord

RECORD_ID = str(uuid.uuid4())
amount = 10.00
note = "Sample Expense"
added_at = datetime.datetime.now()


# todo: add tags later
def mock_data_record():
    return tables.Record(id=RECORD_ID, note=note, amount=amount, type=RecordType.EXPENSE.value,
                         record_book_id=str(uuid.uuid4()), added_at=added_at)


def mock_model_record():
    return ModelRecord(id=RECORD_ID, note=note, amount=amount, type=RecordType.EXPENSE,
                       added_at=added_at)
