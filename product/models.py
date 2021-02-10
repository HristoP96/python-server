from sqlalchemy import Column, Integer, String, DateTime, Sequence
from . import Base
from datetime import datetime


class Product(Base):
    __tablename__ = "products"
    name = Column(String(50), nullable=False, primary_key=True)
    enrolled = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self):
        return f"Product<name={self.name}>"
