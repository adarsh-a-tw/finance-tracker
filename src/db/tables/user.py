from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(String(50), primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(70), nullable=False)
    password = Column(String(70))
    salt = Column(String(70))
    record_books = relationship("RecordBook")

    def __repr__(self):
        return f"User(email={self.email})"
