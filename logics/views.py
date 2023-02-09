from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import *
from .models import *
from rest_framework.response import Response
from django.conf import settings
from accounts.models import *
from django.contrib.auth import get_user_model

User = get_user_model()
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

        try:
            data = request.data
            user = request.user
            serializer = ProductSerializer(data=data)
            group_id = data['group_id']
            group = ClubGroup.objects.get(id=group_id)

            if serializer.is_valid(raise_exception=True) and group:
                # serializer.save()
                if group.group_master == user:
                    product = Product.objects.create(
                        created_by=user, name=data["name"], description=data["description"], price=data["price"])
                    collection = group.collection.add(product)
                    message = {
                        "message": f"Product saved successfully {product}"}
            else:
                message = {"message": serializer.errors}

        except:
            message = {"message": "Please check your data and try again"}
        return Response(message)


class GroupApi(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    authentication_classes = (JWTAuthentication,)
# fetching a particular group and all its data with th
    # def get(self,pk, request, *args, **kwargs):
    #     group = ClubGroup.objects.get(pk=pk)
    #     # validate the group against the user
    #     validate_user = group.members.get(request.user)
    #     if validate_user:
    #         return Response({"group": group})
    #     else:
    #         return Response({"message": "something went wrong or you don't have permission to access this group"})

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            serializer_data = GroupSerializer(data=data)
            if serializer_data.is_valid():
                club = ClubGroup.objects.create(
                    group_master=user, name=data['name'], description=data['description'])
                club.members.add(user)

                response_message = {"message": "Group created successfully"}
            else:
                response_message = {"message": serializer_data.errors}
        except:
            response_message = {"message": "Group creation failed"}

        return Response(response_message)


class GetGroupDetails(generics.RetrieveAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupDetailSerializer
    authentication_classes = (JWTAuthentication,)
# fetching a particular group and all its data and returning only if the person belongs to the group

    def get(self, request, pk):
        group = ClubGroup.objects.get(pk=pk)
        # validate the group against the user
        query = User.objects.filter(email=request.user).first()
        user = UserSerializer(query).data
        print(user['id'])

        data = GroupDetailSerializer(group).data
        user_id = user['id']
        validate_user = group.members.get(pk=user_id)
        print(validate_user)
        # return Response({"group": data})
        if validate_user:
            return Response({"group": data})
        else:
            return Response({"message": "something went wrong or you don't have permission to access this group"})


class GetUserGroup(generics.RetrieveAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupDetailSerializer
    authentication_classes = (JWTAuthentication,)
# fetching all the groups that the user longs to

    def get(self, request):
        try:

            query = User.objects.filter(email=request.user).first()
            user = UserSerializer(query).data
            qr_user = User.objects.get(pk=user['id'])
            # since there is many to many relationship between user and the club group we can use the related name to get all the groupa
            group = qr_user.clubs.all()
            print(group)
            data = GroupDetailSerializer(group, many=True).data
            return Response({"group": data})

        except:
            return Response({"message": "something went wrong or you don't have permission to access this group"})
