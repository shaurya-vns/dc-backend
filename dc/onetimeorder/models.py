from django.db import models
from dc.base_model import BaseModel
from product.models import ProductModel, MealTypeModel
from users.models import UserModel
from product.models import ProductPricingModel
from address.models import AddressModel
from offer.models import OfferModel
import random
import string
from dc.constant import *

class OneTimeOrderModel(BaseModel):

    
    user = models.ForeignKey(
        UserModel,
        related_name="user_one_time_order",
        on_delete=models.CASCADE
    )

    delivery = models.ForeignKey(
        UserModel,
        related_name="delivery_one_time_order",
        limit_choices_to={"userType": UserModel.DELIVERY},
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.PROTECT
    )
 
    address = models.ForeignKey(
        AddressModel,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(default=1)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    final_amount = models.DecimalField(max_digits=10, decimal_places=2)

    offer = models.ForeignKey(
        OfferModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    delivery_date = models.DateField()

    meal_type = models.CharField(max_length=20)

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=PENDING
    )

    rejectReason = models.TextField(
        blank=True,
        null=True
    )

    cancelReason = models.TextField(
        blank=True,
        null=True
    )

    order_number =models.CharField(
            max_length=6,
            unique=True,
            blank=True,
            null=True
        )

    @staticmethod
    def generate_order_number():
        while True:
            code = ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=6
                )
            )
            if not OneTimeOrderModel.objects.filter(order_number=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()

        super().save(*args, **kwargs)