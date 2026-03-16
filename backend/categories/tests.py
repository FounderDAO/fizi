from django.test import TestCase
from rest_framework.test import APIClient
from .models import Category


class TestCategories(TestCase):
    def setUp(self):
        self.client = APIClient()
        Category.objects.create(
            name_ru='Электроника', name_uz='Elektronika', name_en='Electronics',
            slug='electronics', icon='📱', order=1
        )

    def test_category_list(self):
        response = self.client.get('/api/v1/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_category_tree(self):
        response = self.client.get('/api/v1/categories/tree/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
