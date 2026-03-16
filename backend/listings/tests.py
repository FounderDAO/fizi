from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from categories.models import Category
from .models import Listing

User = get_user_model()


class TestListings(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(phone='+998901234567', name='Test')
        self.category = Category.objects.create(
            name_ru='Электроника', name_uz='Elektronika', name_en='Electronics',
            slug='electronics', icon='📱'
        )
        self.listing = Listing.objects.create(
            title='iPhone 13', description='Отличное состояние',
            price=8000000, city='Ташкент', user=self.user,
            category=self.category, status='active'
        )

    def test_listing_list(self):
        response = self.client.get('/api/v1/listings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_listing_detail(self):
        response = self.client.get(f'/api/v1/listings/{self.listing.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'iPhone 13')

    def test_listing_detail_increments_views(self):
        self.client.get(f'/api/v1/listings/{self.listing.pk}/')
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.views, 1)

    def test_create_listing_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/listings/create/', {
            'title': 'Samsung S24',
            'description': 'Новый телефон',
            'price': 12000000,
            'city': 'Ташкент',
            'condition': 'new',
            'category_id': self.category.pk,
        })
        self.assertEqual(response.status_code, 201)

    def test_create_listing_unauthenticated(self):
        response = self.client.post('/api/v1/listings/create/', {'title': 'Test'})
        self.assertEqual(response.status_code, 401)

    def test_favorite_toggle(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f'/api/v1/listings/{self.listing.pk}/favorite/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['favorited'])
        # Toggle off
        response = self.client.post(f'/api/v1/listings/{self.listing.pk}/favorite/')
        self.assertFalse(response.data['favorited'])

    def test_search_by_query(self):
        response = self.client.get('/api/v1/listings/?q=iPhone')
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_city(self):
        response = self.client.get('/api/v1/listings/?city=Ташкент')
        self.assertEqual(response.data['count'], 1)

    def test_my_listings(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/listings/my/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
