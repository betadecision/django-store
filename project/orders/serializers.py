from rest_framework import serializers

from catalog.models import Product

from .models import Order
from .services import create_order


class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=40)
    items = CreateOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "status",
            "total_amount",
            "items",
        ]
        read_only_fields = [
            "id",
            "status",
            "total_amount",
        ]

    def create(self, validated_data):
        return create_order(**validated_data)

