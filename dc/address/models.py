from django.db import models
from dc.base_model import BaseModel
from users.models import UserModel


class AddressModel(BaseModel):

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

    phoneNumber = models.CharField(
        max_length=10,
        
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
        return f"{self.houseNo} - {self.address} - {self.phoneNumber}"