from rest_framework import serializers
from .models import  OrderModel
from subscription.serializers import SubscriptionListSerializer

class OrderListSerializer(serializers.ModelSerializer):

    subscription = SubscriptionListSerializer( read_only=True )
    
    class Meta:
        model = OrderModel
        fields = (
            "id",
            "subscription",
            "meal_type",
            "delivery_date",
            "status",
            'quantity'
        ) 
 