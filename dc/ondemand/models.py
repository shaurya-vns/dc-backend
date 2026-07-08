import random
import string
from dc.base_model import BaseModel
from django.db import models
from users.models import UserModel
from address.models import AddressModel
from dc.constant import *

class OnDemandModel(BaseModel):

   
    PLAN_TYPES = (
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
    )

    mealType = models.CharField(
        max_length=500,
        choices=PLAN_TYPES,
        default="breakfast"
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="on_demand_orders"
    )

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="received_on_demand_orders"
    )

    address = models.ForeignKey(
        AddressModel,
        on_delete=models.PROTECT
    )

    itemName = models.CharField(
        max_length=150
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    deliveryDate = models.DateField()

    userAmount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    vendorAmount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    finalAmount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    image = models.ImageField(
        upload_to="on-demand/",
        blank=True,
        null=True
    )

    note = models.TextField(
        blank=True,
        null=True
    )

    rejectReason = models.TextField(
        blank=True,
        null=True
    )

    cancelReason = models.TextField(
        blank=True,
        null=True
    )

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=PENDING
    )

    orderNumber = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True
    )

    @staticmethod
    def generate_order_number():
        while True:
            code = "OD" + "".join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=6
                )
            )
            if not OnDemandModel.objects.filter(orderNumber=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.orderNumber:
            self.orderNumber = self.generate_order_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.orderNumber} - {self.itemName}"