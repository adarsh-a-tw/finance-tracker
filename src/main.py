import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import InvalidCredentialsException, InvalidAuthTokenException
from src.route.user import router as user_router
from src.route.record_book import router as record_book_router

app = FastAPI()

app.include_router(router=user_router, prefix='/users')
app.include_router(router=record_book_router, prefix='/record_books')


@app.exception_handler(InvalidCredentialsException)
def invalid_credentials_exception_handler(request: Request, ex: InvalidCredentialsException):  # pylint: disable=W0613
    return JSONResponse(status_code=401, content={"message": str(ex)})


@app.exception_handler(InvalidAuthTokenException)
def invalid_auth_token_exception_handler(request: Request, ex: InvalidAuthTokenException):  # pylint: disable=W0613
    return JSONResponse(status_code=403, content={"message": str(ex)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
