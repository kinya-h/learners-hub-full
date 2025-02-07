from rest_framework import serializers
from .models import Payment,WriterProfile,WriterApplication
from rest_framework import viewsets, status
from rest_framework.response import Response
from djoser.serializers import TokenCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username  # Add username to the token
        token['email'] = user.email  # Add email to the token
        return token

class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'tracking_id', 'provider', 'status', 'currency', 
            'amount', 'account', 'phone_number', 'email',
            'first_name', 'last_name' 
        ]
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # Get the user from the request context
        user = self.context['request'].user
        # Add the user to the validated data
        validated_data['user'] = user
        return super().create(validated_data)

class PaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'tracking_id', 'user', 'amount' ,'created_at', 'provider', 'status',
            'currency', 'account', 'phone_number', 'email',
            'first_name', 'last_name'
        ]
        read_only_fields = fields




class WriterApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterApplication
        fields = "__all__"

class WriterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterProfile
        fields = [
            'id', 'avatar', 'name', 'role', 'rating', 'specialization',
            'skills', 'projects', 'experience', 'status', 'location'
        ]