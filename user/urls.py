from django.urls import path
from .api import UsersCrudAPI

urlpatterns = UsersCrudAPI('int').url_patterns
