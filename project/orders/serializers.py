from rest_framework import serializers

from catalog.models import Product

from .models import Order
from .services import create_order


class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(
            category__is_active=True,
            is_active=True,
            stock_quantity__gt=0,
        )
    )
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=40)
    items = CreateOrderItemSerializer(many=True, allow_empty=False)

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

    def validate_items(self, items):
        for item in items:
            product = item["product"]
            quantity = item["quantity"]

            if quantity > product.stock_quantity:
                raise serializers.ValidationError(
                    f"{product.name} has only {product.stock_quantity} item(s) in stock."
                )

        return items

