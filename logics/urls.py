from django.urls import path
from .views import *

app_name = 'logics'
# router = routers.DefaultRouter()
# router.register(r'groups', GroupViewSet)
# router.register(r'groups/(?P<group_id>\d+)/products', ProductViewSet)
urlpatterns = [
    path("product/create", CreateGetProductApi.as_view(), name="Products"),
    path('product/<int:pk>/', ProductApi.as_view(), name='product-detail'),
    path("group/create", CreateGroupApi.as_view(), name="group"),
    path("groupitem/<int:pk>", GetGroupDetails.as_view(), name="group_item"),
    path("all/groups/", GetAllGroups.as_view(), name="groups-details"),
    path("groups/add-member", AddMemberToGroup.as_view(), name="addmember"),
    path('groups/<int:pk>/', GroupApi.as_view(), name='group-api'),
    # path('groups/', GroupApi.as_view()),
    path('groups/remove-member/', RemoveMemberFromGroup.as_view()),
    path('groups/activate-member/', ActivateMember.as_view()),
    path('group/member/request', RequestToJoinGroupView.as_view()),
]
