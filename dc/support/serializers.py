
from datetime import timedelta

from rest_framework import serializers

from .models import SupportTicketModel


class CreateSupportTicketSerializer(serializers.Serializer):

    orderType = serializers.IntegerField(required=True)
    orderId = serializers.IntegerField(required=True)
    issueType = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True)


class SupportTicketDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicketModel
        fields = "__all__"