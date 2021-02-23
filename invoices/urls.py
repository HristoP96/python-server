from .api import InvoicesAPI, get_customers
from django.urls import path

additional_patters = [
    path('c/<int:cluster_id>', get_customers, name="customers")
]
urlpatterns = InvoicesAPI("str").url_patterns + additional_patters