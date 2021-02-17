from django.db.models.expressions import Col
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from json import JSONEncoder
from . import Base
from marshmallow import Schema, fields
from datetime import datetime


class LocationSchema(Schema):
    country = fields.Str()
    city = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()


class UserShchema(Schema):
        first_name = fields.Str()
        last_name = fields.Str()
        email = fields.Str()
        gender = fields.Str()
        location = fields.Nested(LocationSchema())


schema = UserShchema()


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    gender = Column(Enum('M', 'F'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    location = relationship("Location", primaryjoin="and_(User.location_id==Location.id)")

    def __repr__(self):
        customer = dict(first_name=self.first_name, last_name=self.last_name, gender=self.gender, email=self.email, location=self.location)
        return str(schema.dump(customer))


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50))
    city = Column(String(50))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
