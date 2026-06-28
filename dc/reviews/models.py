# review/models.py

from django.db import models

from dc.base_model import BaseModel
from users.models import UserModel
from order.models import OrderModel
from product.models import ProductModel


class ReviewModel(BaseModel):

    order = models.OneToOneField(
        OrderModel,
        on_delete=models.CASCADE,
        related_name="review",
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_reviews",
        limit_choices_to={"userType": UserModel.USER},
    )

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="subowner_reviews",
        limit_choices_to={"userType": UserModel.SUB_OWNER},
    )

    product = models.ForeignKey(
        ProductModel,
        on_delete=models.CASCADE,
        related_name="product_reviews",
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=4.0
    )

    review = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.rating}"