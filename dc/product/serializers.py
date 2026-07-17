from rest_framework import serializers
from .models import ProductModel, ProductPricingModel
from users.models import UserModel
from offer.serializers import OfferSerializer
from users.serializers import UserInfoSerializer


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
    vendorId = serializers.IntegerField(write_only=True)
    pricing_options = ProductPricingSerializer(many=True, required=False)

    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = ProductModel
        fields = (
            "id",
            "vendorId",
            "category",
            "plan_type",
            "name",
            "title",
            "description",
            "is_active",
            "images",
            "pricing_options",
            'offer',
            'product_price'
        )

    def create(self, validated_data):
        pricing_data = validated_data.pop("pricing_options", [])
        vendorId = validated_data.pop("vendorId")

        vendor = UserModel.objects.filter(
            id=vendorId,
            userType=UserModel.VENDOR,
            is_active=True,
        ).first()

        if vendor is None:
            raise serializers.ValidationError({
                "vendorId": "Invalid vendorId."
            })

        product = ProductModel.objects.create(
             vendor = vendor,
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
    isSubscribed = serializers.BooleanField(read_only=True)
    offer = OfferSerializer(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )
    
    class Meta:
        model = ProductModel
        fields = "__all__"


class ProductDetailSerializer(serializers.ModelSerializer):

    pricing_options = ProductPricingSerializer(many=True, read_only=True)
    offer = OfferSerializer(read_only=True)
    vendor = UserInfoSerializer(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    isSubscribed = serializers.BooleanField(read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = ProductModel
        fields = "__all__"
