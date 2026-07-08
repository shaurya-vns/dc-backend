from rest_framework import serializers
from onetimeorder.models import OneTimeOrderModel
from product.serializers import ProductDetailSerializer
from address.serializers import GetAddressSerializer
from offer.serializers import OfferSerializer
from owner.serializers import SubOwnerSerializer
from users.serializers import GetProfileSerializer



class OneTimeOrderCreateSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, default=1)
    isApplyOffer = serializers.BooleanField(default=False)
    addressId = serializers.IntegerField(required=True)

    class Meta:
        model = OneTimeOrderModel
        fields = (
            "product",
            'quantity',
            'isApplyOffer',
            'addressId',
            'delivery_date'
        )

class OneTimeOrderListSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_images = serializers.ListField(
        source="product.images",
        read_only=True
    )

    offer_code = serializers.CharField(
        source="offer.code",
        read_only=True
    )

    class Meta:
        model = OneTimeOrderModel
        fields = "__all__"


from rest_framework import serializers

class OneTimeOrderDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    offer = OfferSerializer(read_only=True)
    address = GetAddressSerializer(read_only=True)
    user = GetProfileSerializer(read_only=True)
    subOwner = SubOwnerSerializer(read_only=True)

    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    final_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = OneTimeOrderModel
        fields = (
            "id",
            "status",
            "user",
            "subOwner",
            "product",
            "quantity",
            "amount",
            "final_amount",
            "offer",
            "address",
            "meal_type",
            "delivery_date",
            'order_number'
        )