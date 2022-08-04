import uuid

from src.service.user import UserService
from src.model.record_book import RecordBook as ModelRecordBook
from src.model.user import User as ModelUser
from src.repository.record_book import RecordBookRepository


class RecordBookService:  # pylint: disable=too-few-public-methods
    def __init__(self, db_session):
        self.repository: RecordBookRepository = RecordBookRepository(db_session=db_session)
        self.user_service: UserService = UserService(db_session=db_session)

    def create_record_book(self, name: str, username: str) -> ModelRecordBook:
        user: ModelUser = self.user_service.fetch_user(username)
        record_book: ModelRecordBook = ModelRecordBook(id=str(uuid.uuid4()), name=name, user=user)
        data_record_book = record_book.data_model()
        self.repository.save(data_record_book)
        return record_book
