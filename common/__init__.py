from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.urls import path
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_engine = create_engine('postgresql+psycopg2://root:root@pg_container_rfm:5432/rfm_db')
Session = sessionmaker(bind=db_engine)
Base = declarative_base()


class CrudAPI:
    def index(self, request: WSGIRequest) -> HttpResponse:
        """Returns all the entities stored in the respective DB from this type of record"""
        pass

    def get(self, request: WSGIRequest, record_id: int) -> HttpResponse:
        """Returns a single entity from the respective DB based on unique id"""
        pass

    def add(self, request: WSGIRequest) -> HttpResponse:
        """Adds an entity to the respective DB"""
        pass

    def delete(self, request: WSGIRequest, record_id: int) -> HttpResponse:
        """Deletes a single entity from the DB based on unique id"""
        pass

    def __init__(self, type: str):
        idType = f'<{type}:record_id>'
        self.url_patterns = [
            path('', self.index, name='index'),
            path(f'{idType}', self.get, name='index'),
            path('a/', self.add, name='append'),
            path(f'd/{idType}/', self.delete, name='delete')
        ]

