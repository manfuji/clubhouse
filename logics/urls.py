from django.urls import path
from .views import *

app_name = 'logics'

urlpatterns = [
    path("product/", ProductApi.as_view(), name="Product"),
    path("group/", GroupApi.as_view(), name="group"),
    path("groupitem/<int:pk>", GetGroupDetails.as_view(), name="group_item"),
    path("allgroups/", GetUserGroup.as_view(), name="groups"),



]
