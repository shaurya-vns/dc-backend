from rest_framework import serializers
from onetimeorder.models import OneTimeOrderModel
from product.serializers import ProductDetailSerializer
from address.serializers import GetAddressSerializer
from offer.serializers import OfferSerializer
from users.serializers import  GetDeliverySerializer, UserBasicInfoSerializer
from django.utils import timezone


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




class OneTimeOrderDetailSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    offer = OfferSerializer(read_only=True)

    delivery = GetDeliverySerializer(read_only=True)

    address = GetAddressSerializer(read_only=True)
    user = UserBasicInfoSerializer(read_only=True)
   
    isToday = serializers.SerializerMethodField()

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
            "product",
            "quantity",
            "amount",
            "final_amount",
            "offer",
            "address",
            "meal_type",
            "delivery_date",
            'order_number',
            "isToday",
            'rejectReason',
            'cancelReason',
            'delivery'
        )

    def get_isToday(self, obj):
        return obj.delivery_date == timezone.localdate()
    


class CancelOneTimeOrderSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
    )



class RejectOneTimeSerializer(serializers.Serializer):
    rejectReason = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
    )