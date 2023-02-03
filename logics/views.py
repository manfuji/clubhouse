from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from .models import *
from rest_framework.response import Response
# Create your views here.
# todo: create logic for
# todo: creating groups and group members with the abilty of only the group masters to add members
# todo: create products and determine complete products


# todo:products
class ProductApi(generics.GenericAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        print(request.user)
        return Response({"message": f"Welcome to the new era {request.user}"})
