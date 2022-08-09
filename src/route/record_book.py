from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi.params import Path
from sqlalchemy.orm import Session

from dependencies import verify_auth, get_session
from dto.create_record_book_response import CreateRecordBookResponse
from dto.create_record_request import CreateRecordRequest
from dto.record_book_info_response import RecordBookInfoResponse
from dto.record_book_list_view_response import RecordBookListViewResponse
from dto.record_info_response import RecordInfoResponse
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


@router.post("/{record_book_id}/records", response_model=RecordInfoResponse, status_code=201)
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


@router.get("", response_model=List[RecordBookListViewResponse], status_code=200)
def fetch_record_books(
        session_class: Session = Depends(get_session),
        user_info: dict = Depends(verify_auth)
):
    with session_class.begin() as session:
        record_book_service = RecordBookService(session)
        record_books: List[ModelRecordBook] = record_book_service.fetch_record_books(username=user_info['username'])
    return list(map(lambda rb: RecordBookListViewResponse(
        id=rb.id,
        name=rb.name,
        net_balance=rb.net_balance(),
        tags=rb.tags()
    ), record_books))


@router.get("/{record_book_id}", response_model=RecordBookInfoResponse, status_code=200)
def fetch_record_book(
        record_book_id: str = Path(title="The ID of the Record Book"),
        session_class: Session = Depends(get_session),
        user_info: dict = Depends(verify_auth)
):
    with session_class.begin() as session:
        record_book_service = RecordBookService(session)
        record_book: [ModelRecordBook] = record_book_service.fetch_record_book(record_book_id=record_book_id,
                                                                               username=user_info['username'])
    return RecordBookInfoResponse(id=record_book.id, name=record_book.name, net_balance=record_book.net_balance(),
                                  tags=record_book.tags(),
                                  records=list(map(lambda r: RecordInfoResponse(
                                      id=r.id,
                                      note=r.note,
                                      amount=r.amount,
                                      type=r.type,
                                      added_at=r.added_at,
                                      tags=r.tags
                                  ), record_book.records())))


@router.delete("/{record_book_id}/records/{record_id}", status_code=204)
def delete_record(
        record_book_id: str = Path(title="The ID of the Record Book"),
        record_id: str = Path(title="The ID of the Record Book"),
        session_class: Session = Depends(get_session),
        user_info: dict = Depends(verify_auth)
):
    with session_class.begin() as session:
        record_book_service = RecordBookService(session)
        record_book_service.delete_record(record_book_id=record_book_id, username=user_info['username'],
                                          record_id=record_id)


@router.delete("/{record_book_id}", status_code=204)
def delete_record(
        record_book_id: str = Path(title="The ID of the Record Book"),
        session_class: Session = Depends(get_session),
        user_info: dict = Depends(verify_auth)
):
    with session_class.begin() as session:
        record_book_service = RecordBookService(session)
        record_book_service.delete_record_book(record_book_id=record_book_id, username=user_info['username'])
