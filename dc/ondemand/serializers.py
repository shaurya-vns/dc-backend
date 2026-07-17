from rest_framework import serializers
from .models import OnDemandModel
from address.serializers import GetAddressSerializer
from users.models import UserModel
from users.serializers import GetDeliverySerializer, UserBasicInfoSerializer, UserInfoSerializer


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

        vendor = UserModel.objects.filter(
           userType=UserModel.VENDOR,
           is_active=True,
       ).first()


        delivery_boy = UserModel.objects.filter(
                        userType=UserModel.DELIVERY,
                        parent = vendor,
                        is_active=True
                    ).first()
                
        return OnDemandModel.objects.create(
            user=user,
            delivery =  delivery_boy, 
            vendor = vendor,
            **validated_data
        )
    
class OnDemandSerializer(serializers.ModelSerializer):

    vendor =  UserInfoSerializer()
    delivery =  GetDeliverySerializer()
    user =  UserBasicInfoSerializer()
    address = GetAddressSerializer()

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



class RejectUserDemandSerializer(serializers.Serializer):
    rejectReason = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=500,
    )

 