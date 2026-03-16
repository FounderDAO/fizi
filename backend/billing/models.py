from django.db import models
from users.models import User
from listings.models import Listing
from shops.models import Shop, SubscriptionPlan


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает'
        SUCCESS = 'success', 'Успешно'
        FAILED = 'failed', 'Ошибка'

    class Type(models.TextChoices):
        SHOP_SUBSCRIPTION = 'shop_sub', 'Подписка магазина'
        LISTING_PROMOTION = 'listing_promo', 'Поднятие объявления'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    payme_transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment #{self.pk} — {self.user} — {self.amount} UZS"

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
