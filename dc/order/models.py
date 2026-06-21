from django.db import models
from dc.base_model import BaseModel
from subscription.models import SubscriptionModel
from product.models import ProductModel, MealTypeModel
from customer.models import CustomerModel

# Create your models here.

class OrderModel(BaseModel):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("out_for_delivery", "Out For Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("skipped", "Skipped"),
    )

    subscription = models.ForeignKey(
        SubscriptionModel,
        related_name="orders",
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE
    )

    meal_type = models.CharField(
        max_length=20,
        choices=MealTypeModel._meta.get_field("name").choices
    )

    delivery_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "subscription",
            "meal_type",
            "delivery_date"
        )
 