
from datetime import timedelta

from rest_framework import serializers

from .models import SubscriptionModel
from order.models import OrderModel

from datetime import timedelta
from product.serializers import ProductDetailSerializer, ProductPricingSerializer


PLAN_TYPE_MAPPING = {
    "breakfast": ["breakfast"],
    "lunch": ["lunch"],
    "dinner": ["dinner"],
    "breakfast_lunch": ["breakfast", "lunch"],
    "breakfast_dinner": ["breakfast", "dinner"],
    "lunch_dinner": ["lunch", "dinner"],
    "breakfast_lunch_dinner": [
        "breakfast",
        "lunch",
        "dinner"
    ],
}


class SubscriptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionModel
        fields = (
            "product",
            "pricing_options",
            "start_date",
        )

    def validate(self, attrs):

        product = attrs["product"]
        pricing_option = attrs["pricing_options"]

        if pricing_option.product_id != product.id:
            raise serializers.ValidationError(
                "Selected pricing option does not belong to selected product."
            )

        attrs["total_days"] = pricing_option.days
        attrs["amount"] = pricing_option.price
        attrs["end_date"] = (
            attrs["start_date"] +
            timedelta(days=pricing_option.days)
        )

        return attrs


def create_subscription_orders(subscription):

    meal_types = PLAN_TYPE_MAPPING.get(
        subscription.product.plan_type,
        []
    )

    current_date = subscription.start_date
    created_days = 0

    while created_days < subscription.total_days:
        for meal_type in meal_types:
            OrderModel.objects.create(
                subscription=subscription,
                user=subscription.user,
                meal_type=meal_type,
                delivery_date=current_date
            )

        created_days += 1
        current_date += timedelta(days=1)


class SubscriptionListSerializer(serializers.ModelSerializer):

    product = ProductDetailSerializer(
        read_only=True
    )

    pricing_detail = ProductPricingSerializer(
        source="pricing_options",
        read_only=True
    )

    class Meta:
        model = SubscriptionModel
        fields = (
            "id",
            "product",
            "pricing_detail",
            "start_date",
            "end_date",
            "total_days",
            "amount",
            "status",
            "created_at",
        )
