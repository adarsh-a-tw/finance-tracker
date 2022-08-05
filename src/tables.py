from sqlalchemy import Column, String, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import relationship

from config.db import DB
from src.model.record_type import RecordType

Base = DB.get_base()


class RecordBookTagMapping(Base): # pylint: disable=too-few-public-methods
    __tablename__ = 'record_book_tag_mapping'
    record_book_id = Column(String(50), ForeignKey("record_book.id"), primary_key=True)
    tag = Column(String(70), primary_key=True)


class RecordTagMapping(Base): # pylint: disable=too-few-public-methods
    __tablename__ = 'record_tag_mapping'
    record_id = Column(String(50), ForeignKey("record.id"), primary_key=True)
    tag = Column(String(70), primary_key=True)


class RecordBook(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = 'record_book'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates="record_books")
    records = relationship("Record", back_populates="record_book")
    net_balance = Column(Float(), default=0)
    tag_map = relationship("RecordBookTagMapping", cascade="all, delete-orphan")

    def __repr__(self):
        return f"RecordBook(name={self.name},user_id={self.user.email})"


class Record(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = 'record'
    id = Column(String(50), primary_key=True)
    note = Column(Text(), nullable=False)
    record_book_id = Column(String(50), ForeignKey('record_book.id'), nullable=False)
    record_book = relationship('RecordBook', back_populates="records")
    amount = Column(Float(), default=0)
    added_at = Column(DateTime())
    type = Column(String(10), default=RecordType.EXPENSE)
    tag_map = relationship("RecordTagMapping", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Record(note={self.note},record_book={self.record_book.name})"


class User(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = 'user'
    id = Column(String(50), primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(70), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    salt = Column(String(100), nullable=False)
    record_books = relationship("RecordBook", back_populates="user")

    def __repr__(self):
        return f"User(email={self.email})"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id and self.username == other.username and \
                   self.email == other.email and self.password == other.password \
                   and self.salt == other.salt
        return False
