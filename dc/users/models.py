from django.db import models
from dc.base_model import BaseModel

# Create your models here.
class UserModel(BaseModel):
    OWNER = 1
    SUB_OWNER = 2
    USER = 3
    DELIVERY = 4

    USER_TYPES = (
        (OWNER, "Owner"),
        (SUB_OWNER, "Sub Owner"),
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
        choices=USER_TYPES
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
    

class UserAddress(BaseModel):

    HOME = 1
    OFFICE = 2
    OTHER = 3

    ADDRESS_TYPES = (
        (HOME, "Home"),
        (OFFICE, "Office"),
        (OTHER, "Other"),
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="addresses",
        limit_choices_to={"userType": UserModel.USER},
        default=UserModel.USER
    )

    addressType = models.IntegerField(
        choices=ADDRESS_TYPES,
        default=HOME,
    )

    houseNo = models.CharField(max_length=100, blank=True)

    landmark = models.CharField(max_length=255, blank=True)

    address = models.TextField(blank=True, )

    city = models.CharField(max_length=100, blank=True,)

    state = models.CharField(max_length=100, blank=True,)

    pincode = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        default=0.0,
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        default=0.0
    )

    isDefault = models.BooleanField(default=True)

    class Meta:
        ordering = ["-isDefault", "-id"]


    def __str__(self):
        return self.address