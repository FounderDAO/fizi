from django.test import TestCase
from .models import Category


class CategoryModelTest(TestCase):
    def test_create_root_category(self):
        cat = Category.objects.create(
            name_ru='Электроника', name_uz='Elektronika', name_en='Electronics',
            slug='electronics'
        )
        self.assertIsNone(cat.parent)
        self.assertTrue(cat.is_active)

    def test_create_child_category(self):
        parent = Category.objects.create(
            name_ru='Электроника', name_uz='Elektronika', name_en='Electronics',
            slug='electronics'
        )
        child = Category.objects.create(
            name_ru='Телефоны', name_uz='Telefonlar', name_en='Phones',
            slug='phones', parent=parent
        )
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children.all())
