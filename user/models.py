from sqlalchemy import Column, Integer, String, DateTime, Sequence
from . import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    enrolled = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self):
        return f"User<name={self.first_name} {self.last_name}>"
