# review/models.py

from django.db import models

from dc.base_model import BaseModel
from users.models import UserModel
from order.models import OrderModel
from product.models import ProductModel


class ReviewModel(BaseModel):

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
    )

    review = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_review",
            )
        ]

    def __str__(self):
        return f"{self.user.name} - {self.rating}"