import uuid
from typing import List, Union

from src.repository.record import RecordRepository
from src.model.record_type import RecordType
from src.service.user import UserService
from src.model.record_book import RecordBook as ModelRecordBook
from src.model.record import Record as ModelRecord
from src.model.user import User as ModelUser
from src.repository.record_book import RecordBookRepository


class RecordBookService:  # pylint: disable=too-few-public-methods
    def __init__(self, db_session):
        self.repository: RecordBookRepository = RecordBookRepository(db_session=db_session)
        self.user_service: UserService = UserService(db_session=db_session)
        self.record_repository: RecordRepository = RecordRepository(db_session=db_session)

    def create_record_book(self, name: str, username: str) -> ModelRecordBook:
        user: ModelUser = self.user_service.fetch_user(username)
        record_book: ModelRecordBook = ModelRecordBook(id=str(uuid.uuid4()), name=name, user=user)
        data_record_book = record_book.data_model()
        self.repository.save(data_record_book)
        return record_book

    def create_record(self, username: str, record_book_id: str, note: str, amount: float,
                      record_type: RecordType,
                      tags: List[str]):
        record_book = self.fetch_record_book(record_book_id, username)
        if not record_book:
            raise Exception  # todo: change to custom exception
        record_id = record_book.add(note, amount, record_type, tags)
        model_record: ModelRecord = record_book.get(record_id)
        self.record_repository.save(model_record.data_model(record_book.id))
        self.repository.update_net_balance(record_book_id, record_book.net_balance())
        return model_record

    def fetch_record_book(self, record_book_id: str, username: str) -> Union[ModelRecordBook, None]:
        user: ModelUser = self.user_service.fetch_user(username)
        if not user:
            raise Exception  # todo: change to custom exception
        data_record_book = self.repository.fetch_record_book(record_book_id, user.id)
        if data_record_book:
            return ModelRecordBook.from_data_model(data_record_book, with_records=True)
        return None
