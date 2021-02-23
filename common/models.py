from django.db.models.expressions import Col
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from json import JSONEncoder
from customer import Base
from marshmallow import Schema, fields
from datetime import datetime


class LocationSchema(Schema):
    country = fields.Str()
    city = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()


class UserShchema(Schema):
        id = fields.Integer()
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
    location = relationship("Location", primaryjoin="and_(Customer.location_id==Location.id)")

    def toJSON(self):
        customer = dict(id=self.id, first_name=self.first_name, last_name=self.last_name, gender=self.gender, email=self.email, location=self.location)
        return schema.dump(customer)


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50))
    city = Column(String(50))
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))


class BrandsSchema(Schema):
    name = fields.Str()


b_schema = BrandsSchema()


class Brands(Base):

    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, primary_key=True)

    def toJSON(self):
        brand = dict(id=self.id, name=self.name)
        return b_schema.dump(brand)


class Invoice_Shchema(Schema):
    product = fields.Nested(BrandsSchema())
    customer = fields.Nested(UserShchema())
    date = fields.Date()
    value = fields.Float()

class Invoice_RFM_Shchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    customer_id = fields.Integer()
    date = fields.Date()
    value = fields.Float()

i_rfm_schema = Invoice_RFM_Shchema()
i_schema = Invoice_Shchema()


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('brands.id'))
    product = relationship("Brands", primaryjoin="and_(Invoice.product_id==Brands.id)")
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship("Customer", primaryjoin="and_(Invoice.customer_id==Customer.id)")
    date = Column(Date)
    value = Column(DECIMAL(12, 2))

    def to_json(self):
        invoice = dict(id=self.id, product=self.product, customer=self.customer, date=self.date, value=self.value)
        return i_schema.dump(invoice)

    def to_rfm_json(self):
        invoice = dict(id=self.id, product_id=self.product_id, customer_id=self.customer_id, date=self.date, value=self.value)
        return i_rfm_schema.dump(invoice)
