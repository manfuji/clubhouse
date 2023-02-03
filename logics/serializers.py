from rest_framework.serializers import ModelSerializer
from .models import *


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "description", "price")


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = ClubGroup
        fields = ("name", "description")


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = ClubGroup
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = MemberVote
        fields = ("vote_product_id", "vote_count")


class ProductSerializer(ModelSerializer):
    class Meta:
        model = MemberVote
        fields = "__all__"
