from .models import UserModel
from rest_framework import serializers
from users.models import UserAddress
 
class CreateUserSerializer(serializers.ModelSerializer):
    subOwnerId = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "phoneNumber",
            "password",
            "platform",
            "deviceToken",
            "deviceId",
            "salt",
            "subOwnerId",
        )

        extra_kwargs = {
            "password": {"write_only": True},
            "salt": {"write_only": True},
        }

    def create(self, validated_data):
        sub_owner_id = validated_data.pop("subOwnerId")

        sub_owner = UserModel.objects.filter(
            id=sub_owner_id,
            userType=UserModel.SUB_OWNER,
            is_active=True,
        ).first()

        if sub_owner is None:
            raise serializers.ValidationError("Invalid SubOwner.")

        validated_data["parent"] = sub_owner
        validated_data["userType"] = UserModel.USER

        return UserModel.objects.create(**validated_data)
    

class LogInSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        ref_name = None


class SubOwnerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "phoneNumber",
            "profileImage",
            "is_active",
        )



class ChangeSubscriptionSerializer(serializers.Serializer):

    subscriptionId = serializers.IntegerField()
    newSubOwnerId = serializers.IntegerField()
    newProductId = serializers.IntegerField()
    newPricingOptionId = serializers.IntegerField()
    startDate = serializers.DateField()



class UserAddressSerializer(serializers.ModelSerializer):

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