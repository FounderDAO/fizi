from celery import shared_task
from django.conf import settings


@shared_task
def send_sms(phone: str, message: str) -> dict:
    """Send SMS via Eskiz."""
    import aiohttp
    import asyncio

    async def _send():
        async with aiohttp.ClientSession() as session:
            # Step 1: Auth
            async with session.post('https://notify.eskiz.uz/api/auth/login', data={
                'email': settings.ESKIZ_EMAIL,
                'password': settings.ESKIZ_PASSWORD,
            }) as resp:
                data = await resp.json()
                token = data.get('data', {}).get('token', '')

            # Step 2: Send
            async with session.post('https://notify.eskiz.uz/api/message/sms/send', headers={
                'Authorization': f'Bearer {token}'
            }, data={
                'mobile_phone': phone,
                'message': message,
                'from': '4546',
            }) as resp:
                return await resp.json()

    return asyncio.run(_send())


@shared_task
def send_push_notification(user_id: int, title: str, body: str, data: dict = None) -> None:
    """Send push notification to user (FCM placeholder)."""
    from notifications.models import Notification
    from users.models import User

    try:
        user = User.objects.get(pk=user_id)
        Notification.objects.create(
            user=user,
            type=data.get('type', 'new_message') if data else 'new_message',
            title=title,
            body=body,
            data=data or {}
        )
    except User.DoesNotExist:
        pass


@shared_task
def cleanup_expired_otps() -> int:
    """Remove OTP codes older than 10 minutes."""
    from django.utils import timezone
    from datetime import timedelta
    from users.models import OTPCode

    cutoff = timezone.now() - timedelta(minutes=10)
    deleted, _ = OTPCode.objects.filter(created_at__lt=cutoff).delete()
    return deleted
