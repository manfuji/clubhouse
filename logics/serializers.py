from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description", "price")


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class GroupSerializer(ModelSerializer):
    class Meta:
        model = ClubGroup
        fields = ("name", "description")


class GroupDetailSerializer(ModelSerializer):
    class Meta:
        depth = 1
        model = ClubGroup
        fields = "__all__"


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
