from users.models import UserModel
from rest_framework import serializers
 

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