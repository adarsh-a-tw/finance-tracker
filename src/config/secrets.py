import os
from dotenv import load_dotenv


def get_secret(secret_name):
    load_dotenv()
    return os.getenv(secret_name)
