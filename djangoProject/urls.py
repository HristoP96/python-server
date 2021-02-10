from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('products/', include('product.urls')),
    path('users/', include('user.urls')),
    path('admin/', admin.site.urls),
]