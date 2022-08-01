from fastapi import FastAPI, Request

from application.decorators import login_required

app = FastAPI()

excluded_paths = [""]


@app.get("/")
@login_required
def hello_world(request: Request):  # pylint:disable=unused-argument
    return {"Hello": "World"}
