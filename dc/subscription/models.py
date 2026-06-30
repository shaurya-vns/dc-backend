from django.db import models
from dc.base_model import BaseModel
from users.models import UserModel, UserAddress
from product.models import ProductModel, ProductPricingModel


# Create your models here.

class SubscriptionModel(BaseModel):

    ACTIVE = 1
    PAUSE =  2
    COMPLETED = 3
    CANCELLED = 4
    TRANSFERRED = 5

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
         (PAUSE, "Pause"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (TRANSFERRED, "Transferred"),
    )


    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.PROTECT
    )

    address = models.ForeignKey(
        UserAddress,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="customer_subscriptions",
        limit_choices_to={"userType": UserModel.SUB_OWNER},
        default=UserModel.SUB_OWNER
    )

    pricing_options = models.ForeignKey(
        ProductPricingModel,
        on_delete=models.PROTECT
    )

    start_date = models.DateField()

    end_date = models.DateField()

    total_days = models.PositiveIntegerField()


    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

    is_active = models.BooleanField(default=True)

    quantity = models.PositiveSmallIntegerField(
        default=1
    )
    
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )



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