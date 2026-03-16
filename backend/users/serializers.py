from rest_framework import serializers
from .models import User, OTPCode, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'avatar', 'bio', 'city', 'is_verified',
                  'rating', 'review_count', 'created_at']
        read_only_fields = ['id', 'is_verified', 'rating', 'review_count', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'avatar', 'bio', 'city', 'is_verified',
                  'rating', 'review_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'phone', 'is_verified', 'rating', 'review_count',
                            'created_at', 'updated_at']


class SendOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)


class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=6)


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'target', 'rating', 'text', 'created_at']
        read_only_fields = ['id', 'reviewer', 'created_at']
