from rest_framework import serializers
from .models import DeliveryTask, ProofOfDelivery


class DeliveryTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTask
        fields = (
            'order',
            'driver_name',
            'status',
        )


class ProofOfDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProofOfDelivery
        fields = (
            'image',
            'otp_verified',
        )
