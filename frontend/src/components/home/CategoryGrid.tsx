import Link from 'next/link';

const categories = [
  { slug: 'electronics', emoji: '📱', name: 'Электроника', nameUz: 'Elektronika', nameEn: 'Electronics' },
  { slug: 'transport', emoji: '🚗', name: 'Транспорт', nameUz: 'Transport', nameEn: 'Transport' },
  { slug: 'realty', emoji: '🏠', name: 'Недвижимость', nameUz: 'Ko\'chmas mulk', nameEn: 'Real Estate' },
  { slug: 'clothing', emoji: '👗', name: 'Одежда', nameUz: 'Kiyim-kechak', nameEn: 'Clothing' },
  { slug: 'furniture', emoji: '🛋️', name: 'Мебель', nameUz: 'Mebel', nameEn: 'Furniture' },
  { slug: 'jobs', emoji: '💼', name: 'Работа', nameUz: 'Ish', nameEn: 'Jobs' },
  { slug: 'services', emoji: '🔧', name: 'Услуги', nameUz: 'Xizmatlar', nameEn: 'Services' },
  { slug: 'kids', emoji: '🧸', name: 'Детские товары', nameUz: 'Bolalar uchun', nameEn: 'Kids' },
  { slug: 'sports', emoji: '⚽', name: 'Спорт', nameUz: 'Sport', nameEn: 'Sports' },
  { slug: 'animals', emoji: '🐾', name: 'Животные', nameUz: 'Hayvonlar', nameEn: 'Animals' },
  { slug: 'garden', emoji: '🌿', name: 'Дача и сад', nameUz: 'Dача va bog\'', nameEn: 'Garden' },
  { slug: 'business', emoji: '📊', name: 'Бизнес', nameUz: 'Biznes', nameEn: 'Business' },
];

export default function CategoryGrid() {
  return (
    <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
      {categories.map((cat) => (
        <Link
          key={cat.slug}
          href={`/ru/listings?category=${cat.slug}`}
          className="flex flex-col items-center gap-2 p-4 bg-white rounded-xl border border-gray-100 hover:border-indigo-300 hover:shadow-md transition-all group"
        >
          <span className="text-3xl group-hover:scale-110 transition-transform">{cat.emoji}</span>
          <span className="text-xs text-center text-gray-700 font-medium leading-tight">{cat.name}</span>
        </Link>
      ))}
    </div>
  );
}
