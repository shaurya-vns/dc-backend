
from datetime import timedelta

from rest_framework import serializers
from contact_us.models import ContactUsModel

 

class CreateContactUsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    subject = serializers.CharField(max_length=150)
    message = serializers.CharField()
    phoneNumber = serializers.CharField()

class UpdateContactStatusSerializer(serializers.Serializer):

    status = serializers.IntegerField()

    adminRemark = serializers.CharField(
        required=False,
        allow_blank=True,
    )

class ContactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContactUsModel
        fields = "__all__"