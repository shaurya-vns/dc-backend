from django.db import models
from dc.base_model import BaseModel
from customer.models import CustomerModel
from product.models import ProductModel, ProductPricingModel, MealTypeModel

# Create your models here.

class SubscriptionModel(BaseModel):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        CustomerModel,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.PROTECT
    )

    pricing_options = models.ForeignKey(
        ProductPricingModel,
        on_delete=models.PROTECT
    )

    start_date = models.DateField()

    end_date = models.DateField()

    total_days = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)



class SubscriptionPause(BaseModel):

    subscription = models.ForeignKey(
        SubscriptionModel,
        related_name="pauses",
        on_delete=models.CASCADE
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField(
        blank=True
    )