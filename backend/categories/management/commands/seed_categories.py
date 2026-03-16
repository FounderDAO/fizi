from django.core.management.base import BaseCommand
from categories.models import Category


CATEGORIES = [
    {'name_ru': 'Электроника', 'name_uz': 'Elektronika', 'name_en': 'Electronics', 'slug': 'electronics', 'icon': '📱', 'order': 1},
    {'name_ru': 'Авто и мото', 'name_uz': 'Avto va moto', 'name_en': 'Auto & Moto', 'slug': 'auto', 'icon': '🚗', 'order': 2},
    {'name_ru': 'Недвижимость', 'name_uz': "Ko'chmas mulk", 'name_en': 'Real Estate', 'slug': 'realty', 'icon': '🏠', 'order': 3},
    {'name_ru': 'Одежда и обувь', 'name_uz': 'Kiyim va poyabzal', 'name_en': 'Clothing', 'slug': 'clothing', 'icon': '👗', 'order': 4},
    {'name_ru': 'Дом и сад', 'name_uz': "Uy va bog'", 'name_en': 'Home & Garden', 'slug': 'home', 'icon': '🏡', 'order': 5},
    {'name_ru': 'Работа', 'name_uz': 'Ish', 'name_en': 'Jobs', 'slug': 'jobs', 'icon': '💼', 'order': 6},
    {'name_ru': 'Услуги', 'name_uz': 'Xizmatlar', 'name_en': 'Services', 'slug': 'services', 'icon': '🔧', 'order': 7},
    {'name_ru': 'Животные', 'name_uz': 'Hayvonlar', 'name_en': 'Animals', 'slug': 'animals', 'icon': '🐾', 'order': 8},
    {'name_ru': 'Детские товары', 'name_uz': 'Bolalar uchun', 'name_en': 'Kids', 'slug': 'kids', 'icon': '🧸', 'order': 9},
    {'name_ru': 'Спорт и хобби', 'name_uz': 'Sport va hobbi', 'name_en': 'Sport', 'slug': 'sport', 'icon': '⚽', 'order': 10},
    {'name_ru': 'Продукты питания', 'name_uz': 'Oziq-ovqat', 'name_en': 'Food', 'slug': 'food', 'icon': '🍎', 'order': 11},
    {'name_ru': 'Бизнес и оборудование', 'name_uz': 'Biznes', 'name_en': 'Business', 'slug': 'business', 'icon': '🏭', 'order': 12},
]


class Command(BaseCommand):
    help = 'Seed categories'

    def handle(self, *args, **kwargs):
        for cat_data in CATEGORIES:
            Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
            self.stdout.write(f"✓ {cat_data['name_ru']}")
        self.stdout.write(self.style.SUCCESS('Categories seeded!'))
