from .models import CustomerModel
from rest_framework import serializers
 

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = [
            'id',
            "name", 
            'platform',
            'deviceToken',
            'deviceId',
            "password", "phoneNumber", "userType", 'salt', 
        ]
        extra_kwargs = {
            "name": {"required": True},
            "phoneNumber": {"required": True},
            "password": {"write_only": True, "required": True},
            "deviceId": {"write_only": True, "required": False},
            "deviceToken": {"write_only": True, "required": False},
            "salt": {"write_only": True, "required": False},
        }


class LogInSwaggerSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        ref_name = None