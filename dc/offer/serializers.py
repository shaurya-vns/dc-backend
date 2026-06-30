from rest_framework import serializers
from .models import OfferModel
from django.utils import timezone


from rest_framework import serializers
 


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfferModel
        fields = "__all__"
        read_only_fields = ("code",) 