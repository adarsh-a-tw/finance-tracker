from fastapi import APIRouter, Depends, Body
from fastapi.params import Path
from sqlalchemy.orm import Session

from dto.create_record_book_response import CreateRecordBookResponse
from dependencies import verify_auth, get_session
from dto.create_record_request import CreateRecordRequest
from dto.create_record_response import CreateRecordResponse
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


@router.post("/{record_book_id}/records", response_model=CreateRecordResponse, status_code=201)
def create_record(
        body: CreateRecordRequest,
        record_book_id: str = Path(title="The ID of the Record Book"),
        session_class: Session = Depends(get_session),
        user_info: dict = Depends(verify_auth)
):
    with session_class.begin() as session:
        record_book_service = RecordBookService(session)
        record = record_book_service.create_record(username=user_info['username'], record_book_id=record_book_id,
                                                   note=body.note, amount=body.amount, record_type=body.type,
                                                   tags=body.tags)
    return record
