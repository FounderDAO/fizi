import ListingCard from './ListingCard';

// Placeholder stub data — will be replaced with API calls
const STUB_LISTINGS = [
  { id: '1', title: 'iPhone 15 Pro 256GB, Natural Titanium', price: 14500000, city: 'Ташкент', date: '16 мар', condition: 'new' as const, views: 234 },
  { id: '2', title: 'Samsung Galaxy S24 Ultra, 512GB, черный', price: 12800000, city: 'Самарканд', date: '15 мар', condition: 'used' as const, views: 187 },
  { id: '3', title: 'MacBook Air M2, 13", 8GB/256GB', price: 18900000, city: 'Ташкент', date: '15 мар', condition: 'new' as const, views: 412 },
  { id: '4', title: 'Toyota Camry 2022, 2.5L, белый', price: 320000000, city: 'Ташкент', date: '14 мар', condition: 'used' as const, views: 891 },
  { id: '5', title: 'PlayStation 5, 825GB, дисковая версия', price: 8500000, city: 'Фергана', date: '14 мар', condition: 'used' as const, views: 156 },
  { id: '6', title: 'Диван угловой, 3+2, серый, IKEA', price: 4200000, city: 'Ташкент', date: '13 мар', condition: 'used' as const, views: 67 },
  { id: '7', title: 'Nike Air Max 270, 42 размер, оригинал', price: 1250000, city: 'Бухара', date: '13 мар', condition: 'new' as const, views: 203 },
  { id: '8', title: 'Холодильник Samsung, No Frost, 200л', price: 5600000, city: 'Ташкент', date: '12 мар', condition: 'used' as const, views: 98 },
];

export default function ListingGrid() {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
      {STUB_LISTINGS.map((listing) => (
        <ListingCard key={listing.id} {...listing} />
      ))}
    </div>
  );
}
