from django.urls import path
from .views import TicketPurchaseView, MpesaCallbackView, TicketValidationView, TicketListView, PaymentTestView

urlpatterns = [
    path('test/', PaymentTestView.as_view(), name='payment-test'),
    path('purchase/', TicketPurchaseView.as_view(), name='ticket-purchase'),
    path('mpesa-callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('validate/', TicketValidationView.as_view(), name='ticket-validate'),
    path('my-tickets/', TicketListView.as_view(), name='my-tickets'),
]