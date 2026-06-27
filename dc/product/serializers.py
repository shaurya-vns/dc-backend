from rest_framework import serializers
from .models import ProductModel, ProductPricingModel
from users.models import UserModel


class ProductPricingSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = ProductPricingModel
        fields = ("id","days", "price", "is_best_offer") 


class ProductCreateSerializer(serializers.ModelSerializer):
    subOwnerId = serializers.IntegerField(write_only=True)
    pricing_options = ProductPricingSerializer(many=True, required=False)

    class Meta:
        model = ProductModel
        fields = (
            "id",
            "subOwnerId",
            "name",
            "plan_name",
            "plan_type",
            "short_description",
            "include",
            "description",
            "is_active",
            "images",
            "pricing_options",
        )

    def create(self, validated_data):
        pricing_data = validated_data.pop("pricing_options", [])
        sub_owner_id = validated_data.pop("subOwnerId")


        sub_owner = UserModel.objects.filter(
            id=sub_owner_id,
            userType=UserModel.SUB_OWNER,
            is_active=True,
        ).first()

        if sub_owner is None:
            raise serializers.ValidationError({
                "subOwnerId": "Invalid SubOwner."
            })

        product = ProductModel.objects.create(
             subOwner=sub_owner,
            **validated_data)
        
        ProductPricingModel.objects.bulk_create([
            ProductPricingModel(
                product=product,
                **price
            )
            for price in pricing_data
        ])


        return product
    


class ProductListSerializer(serializers.ModelSerializer):
    pricing_options = ProductPricingSerializer(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = "__all__"



class ProductDetailSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = ProductModel
        fields = (
            "id",
            "name",
            "plan_name",
            "plan_type",
            "short_description",
            "include",
            "description",
            "images",
            
        )