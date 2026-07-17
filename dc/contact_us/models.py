from django.db import models
from dc.base_model import BaseModel

from users.models import UserModel
  
from dc.constant import *


class ContactUsModel(BaseModel):

    user = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    name = models.CharField(max_length=100)

    phoneNumber = models.CharField(max_length=10)

    subject = models.CharField(max_length=150)

    message = models.TextField()

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    adminRemark = models.TextField(blank=True)