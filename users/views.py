from django.http import JsonResponse, HttpResponse
import json
from .models import User
from . import Session, Base, db_engine
from django.views.decorators.csrf import csrf_exempt

Base.metadata.create_all(db_engine)

session = Session()


def index(request):
    return JsonResponse(session.query(User).all(), safe=False)


@csrf_exempt
def addUser(request):
    f_name = request.POST['first_name']
    l_name = request.POST['last_name']
    u = User(first_name=f_name, last_name=l_name)
    session.add(u)
    session.commit()
    return HttpResponse('User added')


@csrf_exempt
def delete(request, user_id):
    u = session.query(User).get(user_id)
    session.delete(u)
    session.commit()
    return HttpResponse('User delete')

@csrf_exempt
def get(request, user_id):
    u = session.query(User).get(user_id)
    return JsonResponse(u, safe=False)
