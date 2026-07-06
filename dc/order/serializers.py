from rest_framework import serializers
from .models import ProductModel, OrderModel
from product.serializers import ProductDetailSerializer
from users.serializers import CreateUserSerializer
from owner.serializers import SubOwnerSerializer
from subscription.serializers import SubscriptionListSerializer
from users.serializers import UpdateProfileSerializer

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
 