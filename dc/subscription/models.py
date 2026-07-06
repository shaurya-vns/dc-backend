from django.db import models
from dc.base_model import BaseModel
from users.models import UserModel, UserAddress
from product.models import ProductModel, ProductPricingModel
import random
import string

# Create your models here.

class SubscriptionModel(BaseModel):

    PENDING = 1
    ACTIVE = 2
    PAUSED = 3
    COMPLETED = 4
    CANCELLED = 5
    TRANSFERRED = 6
 
    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (ACTIVE, "Active"),
        (PAUSED, "Paused"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
        (TRANSFERRED, "Transferred"),
    )

    PAYMENT_PENDING = 1
    PAYMENT_RECEIVED = 2
    PAYMENT_FAILED = 3
    PAYMENT_REFUNDED = 4

    PAYMENT_STATUS_CHOICES = (
        (PAYMENT_PENDING, "Pending"),
        (PAYMENT_RECEIVED, "Received"),
        (PAYMENT_FAILED, "Failed"),
        (PAYMENT_REFUNDED, "Refunded"),
    )

    payment_status = models.PositiveSmallIntegerField(
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_PENDING,
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

    pricing_options = models.ForeignKey(
        ProductPricingModel,
        on_delete=models.PROTECT
    )

    start_date = models.DateField()

    end_date = models.DateField()


    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE,
    )

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


    sub_number = models.CharField(
            max_length=6,
            unique=True,
            blank=True,
            null=True,
        )

    @staticmethod
    def generate_sub_number():
        while True:
            code = ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=6
                )
            )
            if not SubscriptionModel.objects.filter(sub_number=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.sub_number:
            self.sub_number = self.generate_sub_number()

        super().save(*args, **kwargs)

 



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