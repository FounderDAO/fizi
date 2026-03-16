import random
import string
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPCode, Review
from .serializers import (
    SendOTPSerializer, VerifyOTPSerializer,
    UserProfileSerializer, UserUpdateSerializer, ReviewSerializer
)

User = get_user_model()


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_sms(phone: str, message: str) -> bool:
    """Send SMS via Eskiz.uz. Returns True on success."""
    from django.conf import settings
    import requests

    eskiz_email = getattr(settings, 'ESKIZ_EMAIL', '')
    if not eskiz_email:
        # Dev mode: print OTP to console
        print(f"[DEV SMS] {phone}: {message}")
        return True

    try:
        # Get token
        auth_resp = requests.post(
            'https://notify.eskiz.uz/api/auth/login',
            data={'email': eskiz_email, 'password': settings.ESKIZ_PASSWORD},
            timeout=10
        )
        token = auth_resp.json().get('data', {}).get('token', '')
        if not token:
            return False

        # Send SMS
        resp = requests.post(
            'https://notify.eskiz.uz/api/message/sms/send',
            headers={'Authorization': f'Bearer {token}'},
            data={
                'mobile_phone': phone.replace('+', ''),
                'message': message,
                'from': '4546',
            },
            timeout=10
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"SMS error: {e}")
        return False


class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        # Rate limit: max 3 OTPs per 10 minutes
        recent_count = OTPCode.objects.filter(
            phone=phone,
            created_at__gte=timezone.now() - timedelta(minutes=10),
        ).count()
        if recent_count >= 3:
            return Response(
                {'error': 'Слишком много попыток. Подождите 10 минут.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Generate and save OTP
        code = generate_otp()
        OTPCode.objects.create(phone=phone, code=code)

        # Send SMS
        message = f"Fizi.uz: ваш код подтверждения {code}"
        send_sms(phone, message)

        return Response({'message': 'Код отправлен', 'phone': phone})


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        # Find valid OTP (last 10 minutes, not used)
        otp = OTPCode.objects.filter(
            phone=phone,
            code=code,
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=10),
        ).order_by('-created_at').first()

        if not otp:
            return Response(
                {'error': 'Неверный или истёкший код'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark OTP as used
        otp.is_used = True
        otp.save()

        # Get or create user
        user, created = User.objects.get_or_create(phone=phone)

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserProfileSerializer(user).data,
            'is_new': created,
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.AllowAny]


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(
            target_id=self.kwargs['user_id']
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            reviewer=self.request.user,
            target_id=self.kwargs['user_id']
        )
