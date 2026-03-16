from django.db import models
from users.models import User


class Notification(models.Model):
    class Type(models.TextChoices):
        NEW_MESSAGE = 'new_message', 'Новое сообщение'
        LISTING_SOLD = 'listing_sold', 'Объявление продано'
        PROMOTION_EXPIRED = 'promo_expired', 'Продвижение истекло'
        REVIEW_RECEIVED = 'review_received', 'Получен отзыв'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=30, choices=Type.choices)
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return f"{self.type} → {self.user}"
