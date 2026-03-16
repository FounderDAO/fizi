from django.core.management.base import BaseCommand
from categories.models import Category

CATEGORIES = [
    {
        'name_ru': 'Электроника', 'name_uz': 'Elektronika', 'name_en': 'Electronics',
        'slug': 'electronics', 'icon': '📱', 'order': 1,
        'children': [
            {'name_ru': 'Телефоны', 'name_uz': 'Telefonlar', 'name_en': 'Phones', 'slug': 'phones', 'icon': '📱', 'order': 1},
            {'name_ru': 'Компьютеры', 'name_uz': 'Kompyuterlar', 'name_en': 'Computers', 'slug': 'computers', 'icon': '💻', 'order': 2},
            {'name_ru': 'ТВ и видео', 'name_uz': 'TV va video', 'name_en': 'TV & Video', 'slug': 'tv', 'icon': '📺', 'order': 3},
            {'name_ru': 'Аудиотехника', 'name_uz': 'Audio', 'name_en': 'Audio', 'slug': 'audio', 'icon': '🎧', 'order': 4},
            {'name_ru': 'Фото и видео', 'name_uz': 'Foto va video', 'name_en': 'Photo & Video', 'slug': 'photo', 'icon': '📷', 'order': 5},
            {'name_ru': 'Игры и приставки', 'name_uz': "O'yinlar", 'name_en': 'Gaming', 'slug': 'gaming', 'icon': '🎮', 'order': 6},
            {'name_ru': 'Аксессуары', 'name_uz': 'Aksessuarlar', 'name_en': 'Accessories', 'slug': 'electronics-accessories', 'icon': '🔌', 'order': 7},
        ]
    },
    {
        'name_ru': 'Авто и мото', 'name_uz': 'Avto va moto', 'name_en': 'Auto & Moto',
        'slug': 'auto', 'icon': '🚗', 'order': 2,
        'children': [
            {'name_ru': 'Автомобили', 'name_uz': 'Avtomobillar', 'name_en': 'Cars', 'slug': 'cars', 'icon': '🚗', 'order': 1},
            {'name_ru': 'Мотоциклы', 'name_uz': 'Mototsikllar', 'name_en': 'Motorcycles', 'slug': 'motorcycles', 'icon': '🏍️', 'order': 2},
            {'name_ru': 'Запчасти', 'name_uz': 'Ehtiyot qismlar', 'name_en': 'Spare Parts', 'slug': 'auto-parts', 'icon': '🔧', 'order': 3},
            {'name_ru': 'Грузовики', 'name_uz': 'Yuk mashinalari', 'name_en': 'Trucks', 'slug': 'trucks', 'icon': '🚛', 'order': 4},
        ]
    },
    {
        'name_ru': 'Недвижимость', 'name_uz': "Ko'chmas mulk", 'name_en': 'Real Estate',
        'slug': 'realty', 'icon': '🏠', 'order': 3,
        'children': [
            {'name_ru': 'Квартиры продажа', 'name_uz': 'Kvartiralar sotish', 'name_en': 'Apartments Sale', 'slug': 'apartments-sale', 'icon': '🏢', 'order': 1},
            {'name_ru': 'Квартиры аренда', 'name_uz': 'Kvartiralar ijara', 'name_en': 'Apartments Rent', 'slug': 'apartments-rent', 'icon': '🔑', 'order': 2},
            {'name_ru': 'Дома и дачи', 'name_uz': 'Uylar va dacha', 'name_en': 'Houses', 'slug': 'houses', 'icon': '🏡', 'order': 3},
            {'name_ru': 'Коммерческая', 'name_uz': 'Tijorat', 'name_en': 'Commercial', 'slug': 'commercial', 'icon': '🏪', 'order': 4},
        ]
    },
    {
        'name_ru': 'Одежда и обувь', 'name_uz': 'Kiyim va poyabzal', 'name_en': 'Clothing',
        'slug': 'clothing', 'icon': '👗', 'order': 4,
        'children': [
            {'name_ru': 'Женская одежда', 'name_uz': 'Ayollar kiyimi', 'name_en': 'Women', 'slug': 'women-clothing', 'icon': '👗', 'order': 1},
            {'name_ru': 'Мужская одежда', 'name_uz': 'Erkaklar kiyimi', 'name_en': 'Men', 'slug': 'men-clothing', 'icon': '👔', 'order': 2},
            {'name_ru': 'Детская одежда', 'name_uz': 'Bolalar kiyimi', 'name_en': 'Kids', 'slug': 'kids-clothing', 'icon': '👶', 'order': 3},
            {'name_ru': 'Обувь', 'name_uz': 'Poyabzal', 'name_en': 'Shoes', 'slug': 'shoes', 'icon': '👟', 'order': 4},
        ]
    },
    {
        'name_ru': 'Дом и сад', 'name_uz': "Uy va bog'", 'name_en': 'Home & Garden',
        'slug': 'home', 'icon': '🏡', 'order': 5,
        'children': [
            {'name_ru': 'Мебель', 'name_uz': 'Mebel', 'name_en': 'Furniture', 'slug': 'furniture', 'icon': '🛋️', 'order': 1},
            {'name_ru': 'Бытовая техника', 'name_uz': 'Maishiy texnika', 'name_en': 'Appliances', 'slug': 'appliances', 'icon': '🧺', 'order': 2},
            {'name_ru': 'Сад и огород', 'name_uz': "Bog'", 'name_en': 'Garden', 'slug': 'garden', 'icon': '🌱', 'order': 3},
        ]
    },
    {'name_ru': 'Работа', 'name_uz': 'Ish', 'name_en': 'Jobs', 'slug': 'jobs', 'icon': '💼', 'order': 6, 'children': []},
    {'name_ru': 'Услуги', 'name_uz': 'Xizmatlar', 'name_en': 'Services', 'slug': 'services', 'icon': '🔧', 'order': 7, 'children': []},
    {'name_ru': 'Животные', 'name_uz': 'Hayvonlar', 'name_en': 'Animals', 'slug': 'animals', 'icon': '🐾', 'order': 8, 'children': []},
    {'name_ru': 'Детские товары', 'name_uz': 'Bolalar uchun', 'name_en': 'Kids', 'slug': 'kids', 'icon': '🧸', 'order': 9, 'children': []},
    {'name_ru': 'Спорт и хобби', 'name_uz': 'Sport va hobbi', 'name_en': 'Sport', 'slug': 'sport', 'icon': '⚽', 'order': 10, 'children': []},
    {'name_ru': 'Продукты питания', 'name_uz': 'Oziq-ovqat', 'name_en': 'Food', 'slug': 'food', 'icon': '🍎', 'order': 11, 'children': []},
    {'name_ru': 'Бизнес', 'name_uz': 'Biznes', 'name_en': 'Business', 'slug': 'business', 'icon': '🏭', 'order': 12, 'children': []},
]


class Command(BaseCommand):
    help = 'Seed categories with subcategories'

    def handle(self, *args, **kwargs):
        for cat_data in CATEGORIES:
            children = cat_data.pop('children', [])
            parent, _ = Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
            self.stdout.write(f"✓ {parent.name_ru}")
            for child_data in children:
                child_data['parent'] = parent
                Category.objects.get_or_create(slug=child_data['slug'], defaults=child_data)
                self.stdout.write(f"  └─ {child_data['name_ru']}")
        self.stdout.write(self.style.SUCCESS('Done!'))
