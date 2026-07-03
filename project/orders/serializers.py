
from rest_framework import serializers
from .models import Order, OrderItem
from catalog.models import Product
from .services import create_order

class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    quantity = serializers.IntegerField(min_value=1)
    

class CreateOrderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=40)
    items = CreateOrderItemSerializer(many=True)
    

    def create(self, validated_data):
        return create_order(**validated_data)
             
    



