from rest_framework import serializers

from .models import ReviewModel
from order.models import OrderModel


class ReviewCreateSerializer(serializers.ModelSerializer):

    orderId = serializers.IntegerField(write_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = ReviewModel
        fields = (
            "orderId",
            "rating",
            "review",
        )

    def validate_rating(self, value):

        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5."
            )

        return value
    

class ProductReviewSerializer(serializers.ModelSerializer):

    userName = serializers.CharField(source="user.name", read_only=True)
    subOwnerName = serializers.CharField(source="subOwner.name", read_only=True)

    class Meta:
        model = ReviewModel
        fields = (
            "id",
            "userName",
            "subOwnerName",
            "rating",
            "review",
            "createdAt",
        )