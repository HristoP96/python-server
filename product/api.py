from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from common.models import Brands
from . import Session, Base, db_engine
from django.views.decorators.csrf import csrf_exempt
from common import CrudAPI

Base.metadata.create_all(db_engine)
session = Session()


class BrandsCrudAPI(CrudAPI):

    def index(self, request):
        brands = session.query(Brands).all()
        res = []
        for brand in brands:
            obj = brand.toJSON()
            res.append(obj)
        return JsonResponse(res, safe=False)

    @csrf_exempt
    def add(self, request):
        name = request.POST['name']
        if session.query(Brands).get(name) is not None:
            return HttpResponseBadRequest(f'Product {name} has already been added')
        p = Brands(name=name)
        session.add(p)
        session.commit()
        return HttpResponse(f'Product {name} is added')

    @csrf_exempt
    def delete(self, request, record_id):
        p = session.query(Brands).get(record_id)
        session.delete(p)
        session.commit()
        return HttpResponse(f'Product {p.name} Brand delete')

    @csrf_exempt
    def get(self, request, record_id):
        p = session.query(Brands).get(record_id)
        return JsonResponse(p, safe=False)
