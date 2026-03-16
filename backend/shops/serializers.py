from rest_framework import serializers
from .models import Shop, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price_monthly', 'max_listings', 'has_analytics', 'has_ai']


class ShopSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = [
            'id', 'name', 'slug', 'logo', 'description', 'categories',
            'phone', 'address', 'plan', 'plan_expires_at',
            'is_verified', 'followers_count', 'created_at',
        ]
        read_only_fields = ['id', 'is_verified', 'followers_count', 'created_at']


class ShopCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'slug', 'description', 'phone', 'address', 'categories']
