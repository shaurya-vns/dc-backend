
from datetime import timedelta

from rest_framework import serializers

from .models import SupportMessageModel, SupportTicketModel


class SupportMessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.CharField(
        source="sender.name",
        read_only=True
    )

    class Meta:
        model = SupportMessageModel
        fields = (
            "id",
            "sender",
            "sender_name",
            "message",
            "image",
            "created_at",
        )
        read_only_fields = (
            "sender",
            "created_at",
        )

class SupportTicketSerializer(serializers.ModelSerializer):

    last_message = serializers.SerializerMethodField()

    class Meta:
        model = SupportTicketModel
        fields = (
            "id",
            "subject",
            "issue_type",
            "status",
            "subscription_order",
            "one_time_order",
            "created_at",
            "last_message",
        )

    def get_last_message(self, obj):

        msg = obj.messages.order_by("-created_at").first()

        if msg:
            return msg.message

        return ""
    

class SupportTicketDetailSerializer(serializers.ModelSerializer):

    messages = SupportMessageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = SupportTicketModel
        fields = (
            "id",
            "subject",
            "issue_type",
            "status",
            "subscription_order",
            "one_time_order",
            "messages",
            "created_at",
        )