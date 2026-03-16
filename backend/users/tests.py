from django.test import TestCase
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import User, OTPCode


class TestSendOTP(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('users.views.send_sms', return_value=True)
    def test_send_otp_success(self, mock_sms):
        response = self.client.post('/api/v1/auth/send-otp/', {'phone': '+998901234567'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OTPCode.objects.filter(phone='+998901234567').count(), 1)

    @patch('users.views.send_sms', return_value=True)
    def test_send_otp_rate_limit(self, mock_sms):
        for _ in range(3):
            self.client.post('/api/v1/auth/send-otp/', {'phone': '+998901234567'})
        response = self.client.post('/api/v1/auth/send-otp/', {'phone': '+998901234567'})
        self.assertEqual(response.status_code, 429)


class TestVerifyOTP(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_verify_otp_success(self):
        OTPCode.objects.create(phone='+998901234567', code='123456')
        response = self.client.post('/api/v1/auth/verify-otp/', {
            'phone': '+998901234567', 'code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_verify_otp_wrong_code(self):
        OTPCode.objects.create(phone='+998901234567', code='123456')
        response = self.client.post('/api/v1/auth/verify-otp/', {
            'phone': '+998901234567', 'code': '000000'
        })
        self.assertEqual(response.status_code, 400)

    def test_verify_otp_creates_user(self):
        OTPCode.objects.create(phone='+998987654321', code='654321')
        response = self.client.post('/api/v1/auth/verify-otp/', {
            'phone': '+998987654321', 'code': '654321'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(phone='+998987654321').exists())
        self.assertTrue(response.data['is_new'])


class TestProfile(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(phone='+998901111111', name='Test User')

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/auth/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['phone'], '+998901111111')

    def test_get_profile_unauthenticated(self):
        response = self.client.get('/api/v1/auth/profile/')
        self.assertEqual(response.status_code, 401)

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch('/api/v1/auth/profile/', {'name': 'Updated Name'})
        self.assertEqual(response.status_code, 200)
