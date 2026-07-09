from rest_framework import generics

from .models import Order
from .serializers import CreateOrderSerializer


class CreateOrderView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderSerializer


