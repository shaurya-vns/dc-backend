from rest_framework import serializers
from .models import  OrderModel
from subscription.serializers import SubscriptionListSerializer
from django.utils import timezone

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
        ) 

    def get_isToday(self, obj):
        return obj.delivery_date == timezone.localdate()
 