from django.db import models
from users.models import User
from categories.models import Category


class Listing(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Активно'
        SOLD = 'sold', 'Продано'
        PAUSED = 'paused', 'На паузе'
        MODERATION = 'moderation', 'На модерации'

    class Condition(models.TextChoices):
        NEW = 'new', 'Новое'
        USED = 'used', 'Б/у'

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='UZS')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='listings'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    condition = models.CharField(max_length=10, choices=Condition.choices, default=Condition.USED)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    views = models.IntegerField(default=0)
    is_promoted = models.BooleanField(default=False)
    promoted_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-is_promoted', '-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ListingPhoto(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='listings/')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото объявления'
        verbose_name_plural = 'Фото объявлений'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
