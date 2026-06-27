from datetime import timedelta
from django.db import transaction

from .models import SubscriptionModel
from order.models import OrderModel


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


class SubscriptionService:

    @staticmethod
    @transaction.atomic
    def create_subscription(user, product, pricing_options, start_date):

        total_days = pricing_options.days
        amount = pricing_options.price
        end_date = start_date + timedelta(days=total_days)

        subscription = SubscriptionModel.objects.create(
            user=user,
            total_days = total_days,
            amount = amount,
            start_date=start_date,
            end_date=end_date,
            product=product,
            pricing_options=pricing_options,
            subOwner=product.subOwner
        )

        SubscriptionService.generate_orders(subscription, total_days)

        return subscription

    @staticmethod
    def generate_orders(subscription, total_days):

        meal_types = PLAN_TYPE_MAPPING.get(
            subscription.product.plan_type,
            []
        )

        current_date = subscription.start_date
        orders = []

        for _ in range(total_days):
            for meal_type in meal_types:
                orders.append(
                    OrderModel(
                        subscription=subscription,
                        user=subscription.user,
                        meal_type=meal_type,
                        delivery_date=current_date,
                        subOwner=subscription.subOwner,
                    )
                )
            current_date += timedelta(days=1)

        OrderModel.objects.bulk_create(orders)