from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTPCode, Review

User = get_user_model()


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)

    def validate_phone(self, value):
        # Normalize: remove spaces/dashes and ensure starts with +
        phone = value.replace(' ', '').replace('-', '')
        if not phone.startswith('+'):
            phone = '+' + phone
        return phone


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'avatar', 'bio', 'city',
                  'is_verified', 'rating', 'review_count', 'created_at']
        read_only_fields = ['id', 'phone', 'is_verified', 'rating', 'review_count', 'created_at']


# Alias kept for backward compatibility with other apps (listings, etc.)
UserSerializer = UserProfileSerializer


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'avatar', 'bio', 'city']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.name', read_only=True)
    reviewer_avatar = serializers.ImageField(source='reviewer.avatar', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'reviewer_name', 'reviewer_avatar',
                  'rating', 'text', 'created_at']
        read_only_fields = ['id', 'reviewer', 'created_at']
