from rest_framework import serializers

from .models import ReviewModel
from order.models import OrderModel


class ReviewCreateSerializer(serializers.ModelSerializer):

    productId = serializers.IntegerField(write_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = ReviewModel
        fields = (
            "productId",
            "rating",
            "review",
        )

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value
    

class ReviewSerializer(serializers.ModelSerializer):
    userName = serializers.CharField(source="user.name", read_only=True)
    profileImage = serializers.ImageField(source="user.profileImage", read_only=True)
    rating = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    

    class Meta:
        model = ReviewModel
        fields = (
            "id",
            "userName",
            "profileImage",
            "rating",
            "review",
    
        )