from django.urls import path
from .api import CustomersCrudAPI

customer_patterns = [{

}]
urlpatterns = CustomersCrudAPI('int').url_patterns
