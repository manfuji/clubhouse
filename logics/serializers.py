from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description", "price", "product_mage")


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    class Meta:
        model = ClubGroup
        fields = ("name", "description", "subscription", "club_image")


class GroupDetailSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = ClubGroup
        exclude = ['members']


class MemberVoteSerializer(ModelSerializer):
    class Meta:
        model = MemberVote
        fields = ("vote_product_id", "vote_count")


class MemberVoteSerializer(ModelSerializer):
    class Meta:
        model = MemberVote
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "name", "is_active", "is_staff")


class ClubhouseMemberSerializer(ModelSerializer):
    class Meta:
        model = ClubhouseMember
        fields = "__all__"
