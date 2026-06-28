from users.models import UserModel
from rest_framework import serializers
 
from users.models import UserAddress

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


class SubOwnerAddressSerializer(serializers.ModelSerializer):

    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    pincode = serializers.IntegerField()


    class Meta:
        model = UserAddress
        fields = (
            "id",
            "addressType",
            "houseNo",
            "landmark",
            "address",
            "city",
            "state",
            "pincode",
            "latitude",
            "longitude",
            "isDefault",
        )

    def create(self, validated_data):

        user = self.context["user"]

        if validated_data.get("isDefault", False):
            UserAddress.objects.filter(
                user=user
            ).update(isDefault=False)

        return UserAddress.objects.create(
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):

        if validated_data.get("isDefault", False):
            UserAddress.objects.filter(
                user=instance.user
            ).exclude(id=instance.id).update(isDefault=False)

        return super().update(instance, validated_data)