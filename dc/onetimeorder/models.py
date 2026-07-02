from django.db import models
from dc.base_model import BaseModel
from product.models import ProductModel, MealTypeModel
from users.models import UserModel
from product.models import ProductPricingModel
from users.models import UserAddress
from offer.models import OfferModel


class OneTimeOrderModel(BaseModel):

    PENDING = 1
    ACCEPTED = 2
    PREPARING = 3
    OUT_FOR_DELIVERY = 4
    DELIVERED = 5
    CANCELLED = 6

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (PREPARING, "Preparing"),
        (OUT_FOR_DELIVERY, "Out For Delivery"),
        (DELIVERED, "Delivered"),
        (CANCELLED, "Cancelled"),
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