from django.db import models

# Create your models here.


class CustomerModel(models.Model):
    USER_TYPE_CUSTOMER = 1
    USER_TYPE_DELIVERY = 2

    STATUS_INACTIVE = 0
    STATUS_ACTIVE = 1
    STATUS_AVAILABLE = 2  # Delivery Boy Available

    name = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=10, unique=True,)
    userType = models.IntegerField()  # 1 customer, 2 delivery
    status = models.IntegerField(default=1)    # 2 means delivery available
    platform = models.IntegerField(default=1)
    profileImage = models.CharField(max_length=500, null=True, blank=True)
    deviceToken = models.CharField(max_length=500, default="",null=True, blank=True)
    deviceId = models.CharField(max_length=255, default="", null=True, blank=True)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.phoneNumber or ''}"