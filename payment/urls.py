# urls.py

from django.urls import path
from .views import PaymentView, PaymentCallbackView

app_name = 'payment'

urlpatterns = [
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/callback/', PaymentCallbackView.as_view(),
         name='payment_callback'),
]
