from django.db import models
from dc.base_model import BaseModel
from subscription.models import SubscriptionModel
from product.models import ProductModel, MealTypeModel
from users.models import UserModel

# Create your models here.

class OrderModel(BaseModel):

    PENDING = 1
    ASSIGNED = 2
    OUT_FOR_DELIVERY = 3
    DELIVERED = 4
    CANCELLED = 5
    SKIPPED = 6
    PAUSED = 7

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (ASSIGNED, "Assigned"),
        (OUT_FOR_DELIVERY, "Out For Delivery"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
        (SKIPPED, "Skipped"),
        (PAUSED, "Paused"),
    )

    subscription = models.ForeignKey(
        SubscriptionModel,
        related_name="orders",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="subowner_orders",
        limit_choices_to={"userType": UserModel.SUB_OWNER},
        null=True,
        blank=True,
        )

    meal_type = models.CharField(
        max_length=20,
        choices=MealTypeModel._meta.get_field("name").choices
    )

    delivery_date = models.DateField()


    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)


    quantity = models.PositiveSmallIntegerField(
        default=1
    )

    class Meta:
        unique_together = (
            "subscription",
            "meal_type",
            "delivery_date"
        )
 