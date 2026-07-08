from django.db import models
from dc.base_model import BaseModel

from users.models import UserModel
from order.models import OrderModel
from onetimeorder.models import OneTimeOrderModel

from dc.constant import *


class SupportTicketModel(BaseModel):


    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="support_tickets"
    )

    subOwner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="received_tickets"
    )

    subscription_order = models.ForeignKey(
        OrderModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    one_time_order = models.ForeignKey(
        OneTimeOrderModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    subject = models.CharField(max_length=150)

    issue_type = models.CharField(max_length=50)

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=OPEN
    )

class SupportMessageModel(BaseModel):

    ticket = models.ForeignKey(
        SupportTicketModel,
        related_name="messages",
        on_delete=models.CASCADE
    )

    sender = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    image = models.ImageField(
        upload_to="support/",
        blank=True,
        null=True
    )

    is_read = models.BooleanField(default=False)