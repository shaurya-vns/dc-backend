from django.db import models
from dc.base_model import BaseModel
from product.models import ProductModel, MealTypeModel
from users.models import UserModel
from product.models import ProductPricingModel
from users.models import UserAddress
from offer.models import OfferModel
import random
import string


class OneTimeOrderModel(BaseModel):

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

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="one_time_orders"
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.PROTECT
    )

    address = models.ForeignKey(
        UserAddress,
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