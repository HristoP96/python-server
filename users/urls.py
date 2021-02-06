from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>', views.get, name='index'),
    path('a/', views.addUser, name='append'),
    path('d/<int:user_id>/', views.delete, name='delete')
]