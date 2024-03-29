import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.exceptions import InvalidCredentialsException, InvalidAuthTokenException, PasswordsDontMatchException, \
    EmailInvalidException, EmailAlreadyExistsException, UsernameAlreadyExistsException, RecordBookNotFoundException
from src.route.record_book import router as record_book_router
from src.route.user import router as user_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_router, prefix='/users')
app.include_router(router=record_book_router, prefix='/record_books')


@app.exception_handler(InvalidCredentialsException)
def invalid_credentials_exception_handler(request: Request, ex: InvalidCredentialsException):  # pylint: disable=W0613
    return JSONResponse(status_code=401, content={"message": str(ex)})


@app.exception_handler(InvalidAuthTokenException)
def invalid_auth_token_exception_handler(request: Request, ex: InvalidAuthTokenException):  # pylint: disable=W0613
    return JSONResponse(status_code=403, content={"message": str(ex)})


@app.exception_handler(PasswordsDontMatchException)
def passwords_dont_match_exception_handler(request: Request, ex: PasswordsDontMatchException):  # pylint: disable=W0613
    return JSONResponse(status_code=400, content={"message": str(ex)})


@app.exception_handler(EmailInvalidException)
def email_invalid_exception_handler(request: Request, ex: EmailInvalidException):  # pylint: disable=W0613
    return JSONResponse(status_code=400, content={"message": str(ex)})


@app.exception_handler(EmailAlreadyExistsException)
def email_already_exists_exception_handler(request: Request, ex: EmailAlreadyExistsException):  # pylint: disable=W0613
    return JSONResponse(status_code=400, content={"message": str(ex)})


@app.exception_handler(UsernameAlreadyExistsException)
def username_already_exists_exception_handler(request: Request,  # pylint: disable=W0613
                                              ex: UsernameAlreadyExistsException):
    return JSONResponse(status_code=400, content={"message": str(ex)})


@app.exception_handler(RecordBookNotFoundException)
def record_book_not_found_exception_handler(request: Request,  # pylint: disable=W0613
                                                  ex: RecordBookNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(ex)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
