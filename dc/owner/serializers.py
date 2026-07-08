from users.models import UserModel
from rest_framework import serializers
from address.serializers import GetAddressSerializer
from dc.constant import *

class CreateSubOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = [
            'id',
            "name", 
            'platform',
            'deviceToken',
            'deviceId',
            "password", 
            "phoneNumber",
            'salt',
            'userType'
        ]
        extra_kwargs = {
            "name": {"required": True},
            "phoneNumber": {"required": True},
            "password": {"write_only": True, "required": True},
            "deviceId": {"write_only": True, "required": False},
            "deviceToken": {"write_only": True, "required": False},
            "salt": {"write_only": True, "required": False},
        }


class LoginSubOwnerSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        ref_name = None

  
class SubOwnerSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "phoneNumber",
            "profileImage",
            "address"
        )

    def get_address(self, obj):
        default_address = obj.addresses.filter(isDefault=True).first()

        if not default_address:
            default_address = obj.addresses.first()

        if default_address:
            return GetAddressSerializer(default_address).data

        return None
    

class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices= STATUS_CHOICES
    )
