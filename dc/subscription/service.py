from datetime import timedelta
from django.db import transaction

from .models import SubscriptionModel
from order.models import OrderModel
from django.utils import timezone


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
    def create_subscription(user, product, address, pricing_options, start_date,  quantity=1, isApplyOffer=False):
        
        print('create_subscription ', isApplyOffer)

        total_days = pricing_options.days
        original_price = pricing_options.price * quantity
        
        offer = None
        discount = 0
        if isApplyOffer:
            offer = product.offer  # ONE OFFER PER PRODUCT
            if offer:
                now = timezone.now()
                if (offer.is_active and offer.start_date <= now <= offer.end_date):
                    discount = offer.discount_amount

                 
        final_amount = max(original_price - discount, 0)
        end_date = start_date + timedelta(days=total_days)

        subscription = SubscriptionModel.objects.create(
            user=user,
            subOwner=product.subOwner,
            product=product,
            pricing_options=pricing_options,
            start_date=start_date,
            end_date=end_date,
            total_days=pricing_options.days,
            amount=final_amount,
            original_price = original_price,
            discount_amount = discount,
            quantity=quantity,
            status=SubscriptionModel.ACTIVE,
            address= address
        )

        SubscriptionService.generate_orders(subscription, total_days, quantity)

        return subscription

    @staticmethod
    def generate_orders(subscription, total_days, quantity):

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
                        quantity = quantity
                    )
                )
            current_date += timedelta(days=1)

        OrderModel.objects.bulk_create(orders)