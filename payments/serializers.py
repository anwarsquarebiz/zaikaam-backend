from rest_framework import serializers
from .models import Payment


class CustomerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'amount',
            'status',
            'created_at',
        )

class AdminPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
