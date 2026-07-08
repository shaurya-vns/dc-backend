from django.db import models
from dc.base_model import BaseModel
from users.models import UserModel
from address.models import AddressModel
from product.models import ProductModel, ProductPricingModel
import random
import string

from dc.constant import *

# Create your models here.

class SubscriptionModel(BaseModel):

    payment_status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
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
        AddressModel,
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