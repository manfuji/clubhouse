
from rest_framework.serializers import ModelSerializer
from .models import *


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = '__all__'
