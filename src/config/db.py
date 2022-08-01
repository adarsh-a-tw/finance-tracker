import os

from sqlalchemy import create_engine


class Engine:
    _engine = None

    @staticmethod
    def get_engine():
        if not Engine._engine:
            db_user = os.environ.get("DB_USER", "")
            db_password = os.environ.get("DB_PASS", "")
            db_name = os.environ.get("DB_NAME", "")
            db_host = os.environ.get("DB_HOST", "")
            db_port = os.environ.get("DB_PORT", "")
            Engine._engine = create_engine(
                f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        return Engine._engine
