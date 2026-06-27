from django.db import models
from dc.base_model import BaseModel

from users.models import UserModel
from order.models import OrderModel
from subscription.models import SubscriptionModel


class SupportRequestModel(BaseModel):

    REQUEST_TYPES = (
        ("feedback", "Feedback"),
        ("complaint", "Complaint"),
        ("food_quality", "Food Quality"),
        ("delivery_issue", "Delivery Issue"),
        ("refund", "Refund"),
        ("other", "Other"),
    )

    STATUS_CHOICES = (
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    )

    customer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    order = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE
    )

    subscription = models.ForeignKey(
        SubscriptionModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    request_type = models.CharField(
        max_length=50,
        choices=REQUEST_TYPES
    )

    subject = models.CharField(
        max_length=255
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    admin_remark = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.id} - {self.subject}"