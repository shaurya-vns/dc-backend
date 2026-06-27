
from datetime import timedelta

from rest_framework import serializers

from .models import SupportRequestModel
 
class CreateSupportRequestSerializer(serializers.Serializer):

    orderId = serializers.IntegerField()

    request_type = serializers.ChoiceField(
        choices=[
            "feedback",
            "complaint",
            "food_quality",
            "delivery_issue",
            "refund",
            "other"
        ]
    )

    subject = serializers.CharField()
    message = serializers.CharField()

class SupportRequestListSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True
    )

    class Meta:
        model = SupportRequestModel
        fields = "__all__"


class UpdateSupportRequestSerializer(serializers.Serializer):

    requestId = serializers.IntegerField()

    status = serializers.ChoiceField(
        choices=[
            "open",
            "in_progress",
            "resolved",
            "closed"
        ]
    )

    admin_remark = serializers.CharField()