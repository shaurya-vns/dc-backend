from rest_framework import serializers
from .models import OfferModel
from django.utils import timezone


from rest_framework import serializers
 


class OfferSerializer(serializers.ModelSerializer):

    discount_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = OfferModel
        fields = "__all__"
        read_only_fields = ("code",) 