from django.db import models
from dc.base_model import BaseModel

from users.models import UserModel
  
from dc.constant import *


class SupportTicketModel(BaseModel):

    SUBSCRIPTION = 1
    ONE_TIME = 2
    ON_DEMAND = 3

    ORDER_TYPE_CHOICES = (
        (SUBSCRIPTION, "Subscription"),
        (ONE_TIME, "One Time"),
        (ON_DEMAND, "On Demand"),
    )

    ORDER = 1
    PAYMENT = 2
    DELIVERY = 3
    QUALITY = 4
    REFUND = 5
    OTHER = 6

    ISSUE_TYPE_CHOICES = (
        (ORDER, "Order"),
        (PAYMENT, "Payment"),
        (DELIVERY, "Delivery"),
        (QUALITY, "Food Quality"),
        (REFUND, "Refund"),
        (OTHER, "Other"),
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    orderType = models.IntegerField(choices=ORDER_TYPE_CHOICES, default=ORDER)

    orderId = models.PositiveIntegerField(default=0)

    issueType = models.IntegerField(
        choices=ISSUE_TYPE_CHOICES,
        default= ORDER
    )

    description = models.TextField(default='')

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=OPEN,
    )

    adminRemark = models.TextField(
        blank=True,
        default=''
    )
 