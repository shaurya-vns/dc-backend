from datetime import timedelta

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



def create_subscription_orders(subscription):

    meal_types = PLAN_TYPE_MAPPING.get(
        subscription.product.plan_type,
        []
    )

    current_date = subscription.start_date

    orders = []

    for _ in range(subscription.total_days):

        for meal_type in meal_types:

            orders.append(
                OrderModel(
                    subscription=subscription,
                    user=subscription.user,
                    subOwner=subscription.subOwner,
                    meal_type=meal_type,
                    delivery_date=current_date,
                    status=OrderModel.PENDING,
                )
            )

        current_date += timedelta(days=1)

    OrderModel.objects.bulk_create(orders)