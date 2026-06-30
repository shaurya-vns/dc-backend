from django.db import models
from django.utils import timezone
from dc.base_model import BaseModel
from product.models import ProductModel
from subscription.models import SubscriptionModel
from users.models import UserModel

import random
import string

class OfferModel(BaseModel):

    code = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=255)

    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_active = models.BooleanField(default=True)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not OfferModel.objects.filter(code=code).exists():
                return code
            
    def __str__(self):
        return f"{self.code} - {self.name} - {self.discount_amount}"
        

class OfferUsageModel(models.Model):

    user = models.ForeignKey(
        "users.UserModel",
        on_delete=models.CASCADE
    )

    offer = models.ForeignKey(
        "offer.OfferModel",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        "product.ProductModel",
        on_delete=models.CASCADE
    )

    subscription = models.ForeignKey(
        "subscription.SubscriptionModel",
        on_delete=models.CASCADE
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)