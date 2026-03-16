from django.db import models
from users.models import User
from categories.models import Category


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)  # basic, pro, business
    price_monthly = models.DecimalField(max_digits=12, decimal_places=2)
    max_listings = models.IntegerField(default=50)
    has_analytics = models.BooleanField(default=False)
    has_ai = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тарифный план'
        verbose_name_plural = 'Тарифные планы'


class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='shops/', blank=True, null=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    plan_expires_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    followers_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
