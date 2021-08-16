from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from Customer.models import Customer
from Order.models import Order
from Order.permissions import IsStaffOrOwner
from Order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = IsStaffOrOwner

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            customer = Customer.objects.get(user=self.request.user)
            return Order.objects.filter(customer=customer)
