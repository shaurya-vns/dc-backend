from django.db import models
from dc.base_model import BaseModel

# Create your models here.
class UserModel(BaseModel):
    OWNER = 1
    VENDOR = 2
    USER = 3
    DELIVERY = 4

    USER_TYPES = (
        (OWNER, "Owner"),
        (VENDOR, "Vendor"),
        (USER, "Customer"),
        (DELIVERY, "Delivery"),
    )

    name = models.CharField(max_length=255)

    salt = models.CharField(max_length=255, default='')

    phoneNumber = models.CharField(
        max_length=10,
        unique=True,
    )

    password = models.CharField(max_length=255)

    userType = models.IntegerField(
        choices=USER_TYPES,
        default=USER
    )

    platform = models.IntegerField(
        default=1
    )


    # Parent User
    # SubOwner -> Owner
    # Customer -> SubOwner
    # Delivery -> Owner/SubOwner
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    profileImage = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    deviceToken = models.CharField(
        max_length=500,
        blank=True,
        default=""
    )

    deviceId = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )


    def __str__(self):
        return f"{self.name} ({self.phoneNumber})"