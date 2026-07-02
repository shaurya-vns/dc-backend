from rest_framework import serializers
from product.models import ProductModel, ProductPricingModel
from users.models import UserAddress
from onetimeorder.models import OneTimeOrderModel
from product.serializers import ProductDetailSerializer
from users.serializers import UserAddressSerializer
from offer.serializers import OfferSerializer
from owner.serializers import SubOwnerSerializer



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
    address = UserAddressSerializer(read_only=True)
    subOwner = SubOwnerSerializer(read_only=True)

    class Meta:
        model = OneTimeOrderModel
        fields = (
            "id",
            "created_at",
            "updated_at",

            "status",

            "user",
            "subOwner",

            "product",

            "quantity",

            "amount",
            "discount_amount",
            "final_amount",

            "offer",

            "address",

            "meal_type",
            "delivery_date",
        )