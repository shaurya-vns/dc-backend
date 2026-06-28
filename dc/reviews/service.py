# review/service.py

from django.db import transaction

from .models import ReviewModel
from order.models import OrderModel


class ReviewService:

    @staticmethod
    @transaction.atomic
    def create_review(user, data):


        order = OrderModel.objects.select_related(
            "subscription",
            "subscription__product",
            "user",
            "subOwner",
        ).get(
            id=data["orderId"],
            user=user,
            status=OrderModel.DELIVERED,
        )

        if hasattr(order, "review"):
            raise Exception("Review already submitted.")

        return ReviewModel.objects.create(
            order=order,
            user=user,
            subOwner=order.subOwner,
            product=order.subscription.product,
            rating=data["rating"],
            review=data.get("review", ""),
        )