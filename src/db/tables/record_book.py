from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RecordBook(Base):
    __tablename__ = 'record_book'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=False)
    user_id = Column(String(50), ForeignKey('user.id'), nullable=False)
    user = relationship('User',backref="record_books")

    def __repr__(self):
        return f"RecordBook(name={self.name},user_id={self.user.email})"
