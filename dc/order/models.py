from django.db import models
from dc.base_model import BaseModel
from subscription.models import SubscriptionModel
from product.models import ProductModel, MealTypeModel
from users.models import UserModel
from dc.constant import *

# Create your models here.

class OrderModel(BaseModel):


    subscription = models.ForeignKey(
        SubscriptionModel,
        related_name="orders",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        UserModel,
        related_name="user_orders",
        on_delete=models.CASCADE
    )

    delivery = models.ForeignKey(
        UserModel,
        related_name="delivery_orders",
        limit_choices_to={"userType": UserModel.DELIVERY},
        on_delete=models.SET_NULL,
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

    rejectReason = models.TextField(
        blank=True,
        null=True
    )

    cancelReason = models.TextField(
        blank=True,
        null=True
    )


    class Meta:
        unique_together = (
            "subscription",
            "meal_type",
            "delivery_date"
        )