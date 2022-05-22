from typing_extensions import Final

from flask import Flask

app = Flask("__name__")

HOST: Final = "localhost"
PORT: Final = 8000


@app.route("/")
def index():
    return "Hello"


if __name__ == '__main__':
    app.run(HOST, PORT)
