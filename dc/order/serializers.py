from rest_framework import serializers
from .models import ProductModel, OrderModel
from product.serializers import ProductDetailSerializer

class OrderListSerializer(serializers.ModelSerializer):

    product = ProductDetailSerializer(
        source="subscription.product",
        read_only=True
    )

    class Meta:
        model = OrderModel
        fields = (
            "id",
            "product",
            "meal_type",
            "delivery_date",
            "status",
            "created_at",
            'quantity'
        ) 