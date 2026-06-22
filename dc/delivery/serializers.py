from rest_framework import serializers

class UpdateOrderStatusSerializer(serializers.Serializer):

    orderId = serializers.IntegerField()
    subscriptionId = serializers.IntegerField()

    status = serializers.ChoiceField(
        choices=[
            "pending",
            "assigned",
            "out_for_delivery",
            "delivered",
            "cancelled",
            "skipped"
        ]
    )