# views.py

import requests
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class PaymentView(generics.CreateAPIView):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save()
        payment_url = self.generate_payment_url(payment)

        return Response({'payment_url': payment_url})

    def generate_payment_url(self, payment):
        amount_in_cedis = int(payment.amount * 100)  # Convert amount to cedis
        callback_url = f'{settings.BASE_URL}/api/payment/callback/'

        payload = {
            'amount': amount_in_cedis,
            'email': payment.user.email,
            'callback_url': callback_url,
            'metadata': {
                'payment_id': payment.id,
            },
        }

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.post(
            'https://api.paystack.co/transaction/initialize', json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200 and data['status']:
            return data['data']['authorization_url']

        raise Exception('Failed to generate payment URL')


class PaymentCallbackView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = PaymentSerializer

    def post(self, request):
        payment_id = request.data.get('metadata', {}).get('payment_id')
        if payment_id:
            payment = PaymentModel.objects.get(pk=payment_id)
            verify_payment = self.verify_paystack_payment(
                request.data, payment.amount)

            if verify_payment:
                payment.status = 'completed'
                payment.save()

                return Response({'message': 'Payment successfully verified'})
            else:
                payment.status = 'failed'
                payment.save()

        return Response({'message': 'Payment verification failed'})

    def verify_paystack_payment(self, data, expected_amount):
        reference = data.get('reference')
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}', headers=headers)
        data = response.json()

        if response.status_code == 200 and data['status'] and data['data']['amount'] == expected_amount * 100:
            return True

        return False
