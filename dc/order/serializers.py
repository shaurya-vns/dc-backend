from rest_framework import serializers
from .models import  OrderModel
from subscription.serializers import SubscriptionListSerializer
from django.utils import timezone
from dc.constant import *

class OrderListSerializer(serializers.ModelSerializer):

    subscription = SubscriptionListSerializer( read_only=True )
    isToday = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderModel
        fields = (
            "id",
            "subscription",
            "meal_type",
            "delivery_date",
            "status",
            'quantity',
            "isToday",
            'rejectReason',
            'cancelReason'
        ) 

    def get_isToday(self, obj):
        return obj.delivery_date == timezone.localdate()
    

class CancelOrderSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
    )



class RejectOrderSerializer(serializers.Serializer):
    rejectReason = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
    )
 

class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices= STATUS_CHOICES
    )
