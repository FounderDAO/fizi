from django.test import TestCase
from users.models import User
from categories.models import Category
from .models import Listing, Favorite


class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(phone='+998901234567')
        self.category = Category.objects.create(
            name_ru='Тест', name_uz='Test', name_en='Test', slug='test'
        )

    def test_create_listing(self):
        listing = Listing.objects.create(
            title='Test Listing',
            description='Test description',
            price=100000,
            category=self.category,
            user=self.user,
            city='Tashkent',
        )
        self.assertEqual(listing.status, 'active')
        self.assertEqual(listing.views, 0)
        self.assertFalse(listing.is_promoted)

    def test_favorite_toggle(self):
        listing = Listing.objects.create(
            title='Test', description='Test', price=50000,
            category=self.category, user=self.user, city='Tashkent'
        )
        fav = Favorite.objects.create(user=self.user, listing=listing)
        self.assertTrue(Favorite.objects.filter(user=self.user, listing=listing).exists())
        fav.delete()
        self.assertFalse(Favorite.objects.filter(user=self.user, listing=listing).exists())
