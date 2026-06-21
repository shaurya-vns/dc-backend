from rest_framework import serializers
from .models import ProductModel, ProductPricingModel


class ProductPricingSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = ProductPricingModel
        fields = ("id","days", "price", "is_best_offer") 


class ProductListSerializer(serializers.ModelSerializer):
    pricing_options = ProductPricingSerializer(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = "__all__"



class ProductCreateSerializer(serializers.ModelSerializer):
    pricing_options = ProductPricingSerializer(many=True, required=False)

    class Meta:
        model = ProductModel
        fields = "__all__"

    def create(self, validated_data):
        pricing_data = validated_data.pop("pricing_options", [])
        product = ProductModel.objects.create(**validated_data)

        for price in pricing_data:
            ProductPricingModel.objects.create(
                product=product,
                **price
            )

        return product
    

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