from django.db import models
from dc.base_model import BaseModel
from subscription.models import SubscriptionModel
from product.models import ProductModel, MealTypeModel
from users.models import UserModel
import random
import string

# Create your models here.

class OrderModel(BaseModel):

    PENDING = 1
    PREPARING = 2
    DELIVERED = 3
    CANCELLED = 4
    SKIPPED =  5

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (PREPARING, "Preparing"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
        (SKIPPED, "Skipped"),
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