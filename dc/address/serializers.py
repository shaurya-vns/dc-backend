from users.models import UserModel
from rest_framework import serializers
 
from address.models import AddressModel
 

class AddAddressSerializer(serializers.ModelSerializer):

    latitude = serializers.DecimalField(
        max_digits=10,
        decimal_places =6,
        coerce_to_string=False
    )

    longitude = serializers.DecimalField(
        max_digits=10,
        decimal_places =6,
        coerce_to_string=False
    )
    pincode = serializers.IntegerField()


    class Meta:
        model = AddressModel
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
            AddressModel.objects.filter(
                user=user
            ).update(isDefault=False)

        return AddressModel.objects.create(
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):

        if validated_data.get("isDefault", False):
            AddressModel.objects.filter(
                user=instance.user
            ).exclude(id=instance.id).update(isDefault=False)

        return super().update(instance, validated_data)
    

class GetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = "__all__"
 