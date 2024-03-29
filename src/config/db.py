import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv


class DB:
    _engine = None
    _test_engine = None
    _base = declarative_base()

    @staticmethod
    def get_engine():
        if not DB._engine:
            load_dotenv()
            db_user = os.environ.get("DB_USER", "")
            db_password = os.environ.get("DB_PASS", "")
            db_name = os.environ.get("DB_NAME", "")
            db_host = os.environ.get("DB_HOST", "")
            db_port = os.environ.get("DB_PORT", "")
            DB._engine = create_engine(
                f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        return DB._engine

    @staticmethod
    def get_base():
        return DB._base

    @staticmethod
    def get_session():
        return sessionmaker(DB.get_engine())

    @staticmethod
    def get_test_engine():
        if not DB._test_engine:
            DB._test_engine = create_engine(
                "sqlite:///./test.db", connect_args={"check_same_thread": False}
            )
        return DB._test_engine
