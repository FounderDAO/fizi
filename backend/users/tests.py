import pytest
from django.test import TestCase
from .models import User, OTPCode


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(phone='+998901234567', name='Test User')
        self.assertEqual(user.phone, '+998901234567')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            phone='+998901234568', name='Admin', password='admin123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_otp_creation(self):
        otp = OTPCode.objects.create(phone='+998901234567', code='123456')
        self.assertFalse(otp.is_used)
        self.assertEqual(otp.code, '123456')
