from rest_framework import serializers
from .models import OnDemandModel
from address.serializers import GetAddressSerializer


class OnDemandCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnDemandModel
        fields = (
            "address",
            "itemName",
            "quantity",
            "deliveryDate",
            "mealType",
            "userAmount",
            "note",
        )

    def create(self, validated_data):
        user = self.context["user"]

        print('user sub owner ', user.parent)

        return OnDemandModel.objects.create(
            user=user,
            subOwner = user.parent,
            **validated_data
        )
    
class OnDemandSerializer(serializers.ModelSerializer):

    userName = serializers.CharField(
        source="user.name",
        read_only=True
    )

    userPhone = serializers.CharField(
        source="user.phoneNumber",
        read_only=True
    )

    subOwnerName = serializers.CharField(
        source="subOwner.name",
        read_only=True
    )

    subOwnerPhone = serializers.CharField(
        source="subOwner.phoneNumber",
        read_only=True
    )

    addressDetail = GetAddressSerializer(
        source="address",
        read_only=True
    )

    class Meta:
        model = OnDemandModel
        fields = "__all__"



class UpdateOnDemandSerializer(serializers.ModelSerializer):

    class Meta:
        model = OnDemandModel
        fields = [
            "vendorAmount"
        ]

class CancelUserDemandSerializer(serializers.Serializer):
    cancelReason = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
    )

 