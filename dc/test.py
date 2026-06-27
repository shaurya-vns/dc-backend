import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dc.settings")
django.setup()

from users.models import UserModel
from order.models import OrderModel

print(UserModel.objects.all())


valid_sub_owner = UserModel.objects.filter(
    userType=UserModel.SUB_OWNER
).first()

OrderModel.objects.filter(subOwner__isnull=True).update(
    subOwner=valid_sub_owner
)