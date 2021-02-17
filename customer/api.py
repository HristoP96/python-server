from django.http import JsonResponse, HttpResponse
from .models import Customer
from . import Session, Base, db_engine
from django.views.decorators.csrf import csrf_exempt
from interfaces import CrudAPI
Base.metadata.create_all(db_engine)
session = Session()


class CustomersCrudAPI(CrudAPI):
    def index(self, request):
        users = session.query(Customer).all()
        return HttpResponse(str(users))

    @csrf_exempt
    def add(self, request):
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        u = Customer(first_name=f_name, last_name=l_name)
        session.add(u)
        session.commit()
        return HttpResponse(f'User {f_name} {l_name} is added')

    @csrf_exempt
    def delete(self, request, record_id):
        u = session.query(Customer).get(record_id)
        session.delete(u)
        session.commit()
        return HttpResponse(f'User {u.first_name} {u.last_name} User delete')

    @csrf_exempt
    def get(self, request, user_id):
        u = session.query(Customer).get(user_id)
        return JsonResponse(u, safe=False)
