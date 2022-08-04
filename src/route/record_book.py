from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

from dto.create_record_book_response import CreateRecordBookResponse
from dependencies import verify_auth, get_session
from src.model.record_book import RecordBook as ModelRecordBook
from src.service.record_book import RecordBookService

router = APIRouter()


@router.post("", response_model=CreateRecordBookResponse, status_code=201)
def create_record_book(body: dict = Body(), session_class: Session = Depends(get_session),
                       user_info: dict = Depends(verify_auth)):
    with session_class.begin() as session:
        record_book_service = RecordBookService(session)
        record_book: ModelRecordBook = record_book_service.create_record_book(body['name'], user_info['username'])

    return record_book
