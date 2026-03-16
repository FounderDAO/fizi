from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'type', 'status',
            'shop', 'listing', 'plan',
            'payme_transaction_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class CreatePromotionSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField()
    days = serializers.IntegerField(min_value=1, max_value=30)


class CreateSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
