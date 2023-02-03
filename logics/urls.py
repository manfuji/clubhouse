from django.urls import path
from .views import *

app_name = 'logics'

urlpatterns = [
    path("product/", ProductApi.as_view(), name="Product")
]
