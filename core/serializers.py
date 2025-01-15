from rest_framework import serializers
from .models import Payment

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Payment
from rest_framework import serializers

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['email', 'amount', 'paystack_reference', 'status']
        read_only_fields = ['user']
    def create(self, validated_data):
        print("validated_data")
        # Get the user from the request
        user = self.context['request'].user
        # Add the user to the validated data
        validated_data['user'] = user
        return super().create(validated_data)

class PaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','amount', 'email', 'paystack_reference', 
                 'status', 'created_at']
        read_only_fields = fields

 