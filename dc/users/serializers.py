from .models import UserModel
from rest_framework import serializers
from address.serializers import GetAddressSerializer
 
class CreateUserSerializer(serializers.ModelSerializer):
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
            'userType'
        )

        extra_kwargs = {
            "password": {"write_only": True},
            "salt": {"write_only": True},
        }

    def create(self, validated_data):
       vendor = UserModel.objects.filter(
           userType=UserModel.VENDOR,
           is_active=True,
       ).first()
       validated_data["parent"] = vendor
       
       return UserModel.objects.create(**validated_data)
    

class LogInSerializer(serializers.Serializer):
    phoneNumber = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        ref_name = None


class ChangeSubscriptionSerializer(serializers.Serializer):

    subscriptionId = serializers.IntegerField()
    newSubOwnerId = serializers.IntegerField()
    newProductId = serializers.IntegerField()
    newPricingOptionId = serializers.IntegerField()
    startDate = serializers.DateField()


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = [
            "name",
            "profileImage"
        ]

class GetDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "phoneNumber",
            'userType'
        )

class UserListSerializer(serializers.ModelSerializer):
    subscription_order_count = serializers.IntegerField(read_only=True)
    one_time_order_count = serializers.IntegerField(read_only=True)
    total_order_count = serializers.IntegerField(read_only=True)
    

    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "phoneNumber",
            "subscription_order_count",
            "one_time_order_count",
            "total_order_count",
           
        )

  
class UserInfoSerializer(serializers.ModelSerializer):
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

class UserBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = (
            "id",
            "name",
            "phoneNumber",
            'userType'
        )