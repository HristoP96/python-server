from django.http import JsonResponse, HttpResponse
from common.models import Customer
from common import Session
from django.views.decorators.csrf import csrf_exempt
from common import CrudAPI

session = Session()


class CustomersCrudAPI(CrudAPI):
    cache = []

    def index(self, request):
        if len(self.cache) != 0:
            return JsonResponse(self.cache, safe=False)

        users = session.query(Customer).all()
        res = []
        for user in users:
            obj = user.toJSON()
            res.append(obj)
        cache = res
        return JsonResponse(res, safe=False)

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
