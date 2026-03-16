import random
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTPCode, Review
from .serializers import (
    UserSerializer, UserProfileSerializer,
    SendOTPSerializer, VerifyOTPSerializer, ReviewSerializer
)


class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        # Generate OTP
        code = str(random.randint(100000, 999999))
        OTPCode.objects.create(phone=phone, code=code)

        # TODO: Send via Eskiz SMS
        # For dev, return code in response
        return Response({'message': 'OTP sent', 'dev_code': code}, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']

        otp = OTPCode.objects.filter(
            phone=phone, code=code, is_used=False
        ).order_by('-created_at').first()

        if not otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark as used
        otp.is_used = True
        otp.save()

        # Get or create user
        user, created = User.objects.get_or_create(phone=phone)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
            'is_new': created,
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(target_id=self.kwargs['user_id'])

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
