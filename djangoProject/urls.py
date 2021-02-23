from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('brands/', include('product.urls')),
    path('users/', include('customer.urls')),
    path('invoices/', include('invoices.urls')),
    path('admin/', admin.site.urls)
]