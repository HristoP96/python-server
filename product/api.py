from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Product
from . import Session, Base, db_engine
from django.views.decorators.csrf import csrf_exempt
from interfaces import CrudAPI

Base.metadata.create_all(db_engine)
session = Session()


class ProductsCrudAPI(CrudAPI):
    def index(self, request):
        return JsonResponse(session.query(Product).all(), safe=False)

    @csrf_exempt
    def add(self, request):
        name = request.POST['name']
        if session.query(Product).get(name) is not None:
            return HttpResponseBadRequest(f'Product {name} has already been added')
        p = Product(name=name)
        session.add(p)
        session.commit()
        return HttpResponse(f'Product {name} is added')

    @csrf_exempt
    def delete(self, request, record_id):
        p = session.query(Product).get(record_id)
        session.delete(p)
        session.commit()
        return HttpResponse(f'Product {p.name} User delete')

    @csrf_exempt
    def get(self, request, record_id):
        p = session.query(Product).get(record_id)
        return JsonResponse(p, safe=False)
