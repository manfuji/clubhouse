from django.core.exceptions import ObjectDoesNotExist
from .views import *
from django.urls import path
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
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from .util_send_mail import send_email
from datetime import datetime, timedelta
import requests

User = get_user_model()

# Create your views here.
# Create logic for
# Creating groups and group members with the abilty of only the group masters to add members
# Create products and determine complete products


# products

class ProductApi(generics.GenericAPIView):
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    parser_classes = [MultiPartParser, FormParser]

    def delete(self, request, pk):
        try:
            product = self.get_product(pk)
            group = self.get_group(request.data.get('group_id'))
            self.check_group_master(group, request.user)

            product.delete()
            self.notify_group_members(group)
            return Response({"message": "Product deleted successfully"})

        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_product(self, pk):
        return Product.objects.get(pk=pk)

    def get_group(self, group_id):
        try:
            return ClubGroup.objects.get(id=group_id)
        except ClubGroup.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def check_group_master(self, group, user):
        if group.group_master != user:
            return Response({"message": "You are not authorized to delete this product"}, status=status.HTTP_403_FORBIDDEN)

    def notify_group_members(self, group):
        subject = "Message from Tiwdo"
        message = f"A product has been deleted from a group you are part of. group name: {group.name}"
        group_members = group.get_members()
        for member in group_members:
            send_email(subject, message, recipient_list=[member.user.email])

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            user = request.user
            data = request.data

            group_id = data['group_id']
            # group = ClubGroup.objects.get(id=group_id)
            group = self.get_group(self, group_id)

            self.very_group_master(self, group, user)
            if group.group_master == user:
                serializer = ProductSerializer(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "You are not authorized to update this product"}, status=status.HTTP_403_FORBIDDEN)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def very_group_master(self, group, user):
        if group.group_master != user:
            return Response({"message": "You are not authorized to update this product"}, status=status.HTTP_403_FORBIDDEN)

    def get_group(self, group_id):
        try:
            return ClubGroup.objects.get(id=group_id)
        except ClubGroup.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

# products


class CreateGetProductApi(generics.GenericAPIView):
    """
    Create a new product using this route
    """
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    authentication_classes = (JWTAuthentication,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        message = {"message": "Please check your data and try again"}
        try:
            data = request.data
            print(data)
            user = request.user
            serializer = ProductSerializer(data=data)
            group_id = data['group_id']
            group = ClubGroup.objects.get(id=group_id)
            if serializer.is_valid(raise_exception=True) and group:
                # serializer.save()
                if group.group_master == user:
                    product = Product.objects.create(
                        created_by=user, name=data["name"], description=data["description"], price=data["price"], product_mage=data["image"])
                    group.collection.add(product)
                    # def notify_group_members(self, group):
                    subject = "Message from Tiwdo"
                    message = f"A product has been created in a group you are part of. group name: {group.name}"
                    group_members = group.get_members()
                    for member in group_members:
                        send_email(subject, message, recipient_list=[
                                   member.user.email])
                    message = {
                        "message": "Product saved successfully"}
                    return Response(message, status=status.HTTP_201_CREATED)
            else:
                message = {"message": serializer.errors}

        except Exception as e:
            message = {
                "message": f"Please check your data and try again {e}"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class GroupApi(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    authentication_classes = (JWTAuthentication,)
    parser_classes = [MultiPartParser, FormParser]

    def perform_destroy(self, instance):
        instance.delete()

    def put(self, request, *args, **kwargs):
        data = request.data

        try:

            group_id = data['group_id']
            group = ClubGroup.objects.get(id=group_id)
            if group.group_master != request.user:
                response_message = {
                    "message": "You are not allowed to update this group."}
                return Response(response_message, status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(group, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_message = {"message": "Group updated successfully"}
            return Response(response_message, status=status.HTTP_200_OK)
        except Exception as e:
            response_message = {f"message": "Group not found {e}"}
            return Response(response_message, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        data = request.data

        try:

            group_id = data['group_id']
            group = ClubGroup.objects.get(id=group_id)
            if group.group_master != request.user:
                response_message = {
                    "message": "You are not allowed to delete this group."}
                return Response(response_message, status=status.HTTP_403_FORBIDDEN)

            self.perform_destroy(group)

            response_message = {"message": "Group deleted successfully"}
            return Response(response_message, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            response_message = {f"message": "Group not found {e}"}

            return Response(response_message, status=status.HTTP_404_NOT_FOUND)


class CreateGroupApi(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer
    authentication_classes = (JWTAuthentication,)
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        try:
            serializer_data = GroupSerializer(data=data)
            if serializer_data.is_valid():
                club = ClubGroup.objects.create(
                    group_master=user, name=data['name'], description=data['description'], subscription=data['subscription'], club_image=data['image'])
                club.members.add(user)

                response_message = {"message": "Group created successfully"}
            else:
                response_message = {"message": serializer_data.errors}
        except Exception as e:
            response_message = {"message": f"Group creation failed; {e}"}

        return Response(response_message)


class GetGroupDetails(generics.RetrieveAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupDetailSerializer
    authentication_classes = (JWTAuthentication,)

    def get(self, request, pk):
        try:
            group = ClubGroup.objects.get(pk=pk)
            user = request.user
            user_id = user.id
            validate_user = group.get_members().filter(pk=user_id).first()

            if (group.members.filter(pk=user_id).exists() and validate_user and validate_user.active) or group.group_master == user:
                group_data = GroupDetailSerializer(group).data
                members = group.get_members()
                member_data = ClubhouseMemberSerializer(
                    members, many=True).data
                data_with_members = {
                    "group": {**group_data, "members": member_data}}
                return Response(data_with_members)
            else:
                return Response({"message": "You don't have permission to access this group."})
        except ClubGroup.DoesNotExist:
            return Response({"message": "Invalid group ID."})

# class GetAllGroups(generics.GenericAPIView):
#     queryset = ClubGroup.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = GroupDetailSerializer
#     authentication_classes = (JWTAuthentication,)
# # fetching all the groups that the user longs to

#     def get(self, request):
#         try:

#             query = User.objects.filter(email=request.user).first()
#             user = UserSerializer(query).data
#             qr_user = User.objects.get(pk=user['id'])
#             # since there is many to many relationship between user and the club group we can use the related name to get all the groupa
#             group = qr_user.clubs.all()
#             # members = qr_user.get_()
#             print(group.get_members())
#             data = GroupDetailSerializer(group, many=True).data
#             return Response({"group": data})

#         except Exception as e:
#             return Response({"message": f"something went wrong {e}"})


class GetAllGroups(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupDetailSerializer
    authentication_classes = (JWTAuthentication,)

    def get(self, request):
        try:
            query = User.objects.filter(email=request.user).first()
            user = UserSerializer(query).data
            qr_user = User.objects.get(pk=user['id'])
            groups = qr_user.clubs.all()
            data = []
            for group in groups:
                members = group.get_members()
                group_data = GroupDetailSerializer(group).data
                # Convert members queryset to list of dictionaries
                group_data['members'] = members.values()
                data.append(group_data)
            return Response({"groups": data})
        except Exception as e:
            return Response({"message": f"something went wrong {e}"})


class AddMemberToGroup(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data

            group_id = data.get('group_id')
            new_member_email = data.get('new_member')
            subscription_type = data.get('subscription_type')

            if not group_id:
                return Response({"message": "Group ID is required."})

            if not new_member_email:
                return Response({"message": "New member email is required."})

            try:
                group = ClubGroup.objects.get(id=group_id)
            except ObjectDoesNotExist:
                return Response({"message": "Invalid group ID."})

            verify_user = group.group_master
            if verify_user != user:
                return Response({"message": "You don't have permission to add members to this group."})

            try:
                new_member = User.objects.get(email=new_member_email)
            except ObjectDoesNotExist:
                return Response({"message": "Invalid user email."})

            current_date = datetime.now().date()
            expiration_date = current_date + timedelta(days=30)

            member = ClubhouseMember.objects.create(
                user=new_member, club=group, subscription_type=subscription_type, subscription_expiration_date=expiration_date, active=True)
            group.members.add(new_member)

            subject = "Tiwdo Group Welcome message"
            message = f"Welcome {new_member} to {group.name}"
            send_email(subject, message, recipient_list=[new_member_email])

            return Response({"message": f"Successfully added {new_member} to {group.name}"})

        except Exception as e:
            return Response({"message": f"Failed to add new member: {str(e)}"})


class ActivateMember(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        message = {"message": "Please check your data and try again"}
        try:
            user = request.user
            data = request.data
            group = ClubGroup.objects.get(id=data['group_id'])
            verify_user = group.group_master

            if verify_user == user:
                member_to_activate = User.objects.get(
                    email=data['member_email'])

                user_to_activate = ClubhouseMember.objects.filter(
                    user=member_to_activate).first()
                user_to_activate.active = True
                user_to_activate.save()  # Save the changes to the database

                message = {"message": "Member activated successfully"}
                subject = "Activation message from Tiwdo"
                email_message = f"Congratulations! Your account with the email {member_to_activate} has been activated again for {group.name}. Enjoy your membership!"
                send_email(subject, email_message, recipient_list=[
                           member_to_activate.email])
            else:
                message = {
                    "message": "You are not authorized to activate a member in this group"}
        except Exception as e:
            message = {"message": f"Failed to activate member: {e}"}

        return Response(message)


class RemoveMemberFromGroup(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        message = {"message": "Please check your data and try again"}
        try:
            user = request.user
            data = request.data
            group = ClubGroup.objects.get(id=data['group_id'])
            verify_user = group.group_master

            if verify_user == user:
                member_to_remove = User.objects.get(email=data['member_email'])
                # group.members.remove(member_to_remove)

                user_to_deactivate = ClubhouseMember.objects.filter(
                    user=member_to_remove).first()
                user_to_deactivate.active = False
                user_to_deactivate.save()
                message = {"message": "Member removed successfully"}
                subject = "Dismisal message from Tiwdo"
                message = f"Alert!! your account with the email {member_to_remove} has been removed from  {group.name} contact group administrator @ {verify_user}"
                send_email(subject, message,
                           recipient_list=[member_to_remove])
            else:
                message = {
                    "message": "You are not authorized to remove a member from this group"}
        except Exception as e:
            message = {"message": f"Failed to remove member from group: {e}"}

        return Response(message)


class VotingProduct(generics.GenericAPIView):
    queryset = ClubGroup.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def post(self, request):
        group = ClubGroup.objects.get(pk=request.data['group_id'])
        # validate the group against the user
        product_id = request.data['product_id']
        query = User.objects.filter(email=request.user).first()
        user = UserSerializer(query).data
        print(user['id'])

        # data = GroupDetailSerializer(group).data
        user_id = user['id']
        validate_user = group.members.get(pk=user_id)
        # cast vote

        print(validate_user)
        # return Response({"group": data})
        product = group.collection.get(pk=product_id)
        if validate_user and product:
            # product.vote_count += 1
            # product.save()
            fetch_product = Product.objects.get(pk=product_id)
            fetch_product.vote_count += 1
            fetch_product.save()

            return Response({"msg": "vote casted"})
        else:
            return Response({"message": "something went wrong or you don't have permission to access this group"})


class RequestToJoinGroupView(generics.GenericAPIView):
    queryset = RequestToJoinGroup.objects.all()
    serializer_class = RequestToJoinGroupSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        if not user and data:
            return Response({"message": "You are not logged in or the all the fields are requested."})
        try:
            group = ClubGroup.objects.filter(id=data['id'])

            if not group:
                return Response({"message": "Invalid group ID"})

            self.check_group_master(group, user)
            data = RequestToJoinGroup.objects.filter(club_group=group)
            serilaized_data = RequestToJoinGroupSerializer(data).data
            return Response({"requests": serilaized_data})
        except Exception as e:
            return Response({"message": f"something went wrong {e}"})

    def post(self, request, *args, **kwargs):
        data = request.data

        group_id = data['group_id']
        new_member_email = data['new_member']

        if not group_id:
            return Response({"message": "Group ID is required."})
        if not new_member_email:
            return Response({"message": "New member email is required."})

        try:
            group = ClubGroup.objects.get(id=group_id)
            verify_user = User.objects.get(email=new_member_email)
            if not verify_user or not group:
                return Response({"message": "Invalid group ID or user email."})
            savedData = RequestToJoinGroup.objects.create(
                user=verify_user, club_group=group)
            subject = "Tiwdo message for joining a group"
            message = f"Your request to join {group} is pending we will let you know when your request is approved"
            recipient = [new_member_email]
            send_email(subject, message, recipient_list=recipient)
            return Response({"message": f"Successfully added {new_member_email} to {group.name} but pending."})

        except Exception as e:
            return Response({"message": f"Invalid data {e}."})

    def put(self, request, *args, **kwargs):
        request_id = kwargs.get('id')
        data = request.data

        try:
            request_instance = RequestToJoinGroup.objects.get(id=request_id)

            serializer = RequestToJoinGroupSerializer(
                request_instance, data=data, partial=True)
            if serializer.is_valid():
                updated_request = serializer.save()
                return Response(RequestToJoinGroupSerializer(updated_request).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except RequestToJoinGroup.DoesNotExist:
            return Response({"message": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": f"Something went wrong: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def check_group_master(self, group, user):
        if group.group_master != user:
            return Response({"message": "You are not authorized to delete this product"}, status=status.HTTP_403_FORBIDDEN)
