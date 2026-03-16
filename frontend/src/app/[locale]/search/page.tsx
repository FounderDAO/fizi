'use client';

import { useSearchParams, useRouter } from 'next/navigation';
import { useState, useEffect, Suspense } from 'react';
import { useLocale, useTranslations } from 'next-intl';
import { Search, SlidersHorizontal, X } from 'lucide-react';
import ListingGrid from '@/components/listings/ListingGrid';
import api from '@/lib/api';

function SearchContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const locale = useLocale();

  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [category, setCategory] = useState(searchParams.get('category') || '');
  const [city, setCity] = useState(searchParams.get('city') || '');
  const [priceMin, setPriceMin] = useState(searchParams.get('price_min') || '');
  const [priceMax, setPriceMax] = useState(searchParams.get('price_max') || '');
  const [condition, setCondition] = useState(searchParams.get('condition') || '');
  const [hasPhoto, setHasPhoto] = useState(searchParams.get('has_photo') === 'true');
  const [showFilters, setShowFilters] = useState(false);
  const [categories, setCategories] = useState<any[]>([]);

  useEffect(() => {
    api.get('/categories/').then(res => setCategories(res.data));
  }, []);

  const buildParams = () => {
    const params: any = {};
    if (query) params.q = query;
    if (category) params.category = category;
    if (city) params.city = city;
    if (priceMin) params.price_min = priceMin;
    if (priceMax) params.price_max = priceMax;
    if (condition) params.condition = condition;
    if (hasPhoto) params.has_photo = 'true';
    return params;
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams(buildParams());
    router.push(`/${locale}/search?${params}`);
  };

  const clearFilters = () => {
    setCategory(''); setCity(''); setPriceMin(''); setPriceMax(''); setCondition(''); setHasPhoto(false);
  };

  const filterParams = buildParams();

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Search bar */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-6">
        <div className="flex-1 flex items-center border rounded-xl bg-white px-4 gap-2">
          <Search className="w-5 h-5 text-gray-400" />
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Поиск..."
            className="flex-1 py-3 outline-none text-gray-800"
          />
        </div>
        <button type="submit" className="bg-indigo-600 text-white px-6 rounded-xl font-semibold hover:bg-indigo-700">
          Найти
        </button>
        <button
          type="button"
          onClick={() => setShowFilters(!showFilters)}
          className="border rounded-xl px-4 flex items-center gap-2 hover:bg-gray-50"
        >
          <SlidersHorizontal className="w-5 h-5" />
        </button>
      </form>

      {/* Filters panel */}
      {showFilters && (
        <div className="bg-white rounded-xl border p-4 mb-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <select value={category} onChange={e => setCategory(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm">
            <option value="">Все категории</option>
            {categories.map((c: any) => (
              <option key={c.id} value={c.slug}>{c.name_ru}</option>
            ))}
          </select>
          <input value={city} onChange={e => setCity(e.target.value)}
            placeholder="Город" className="border rounded-lg px-3 py-2 text-sm" />
          <input value={priceMin} onChange={e => setPriceMin(e.target.value)}
            placeholder="Цена от" type="number" className="border rounded-lg px-3 py-2 text-sm" />
          <input value={priceMax} onChange={e => setPriceMax(e.target.value)}
            placeholder="Цена до" type="number" className="border rounded-lg px-3 py-2 text-sm" />
          <select value={condition} onChange={e => setCondition(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm">
            <option value="">Любое состояние</option>
            <option value="new">Новое</option>
            <option value="used">Б/у</option>
          </select>
          <label className="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" checked={hasPhoto} onChange={e => setHasPhoto(e.target.checked)}
              className="w-4 h-4 accent-indigo-600" />
            <span className="text-sm">Только с фото</span>
          </label>
          <button onClick={clearFilters} className="flex items-center gap-1 text-red-500 text-sm">
            <X className="w-4 h-4" /> Сбросить
          </button>
        </div>
      )}

      {/* Results */}
      <ListingGrid filters={filterParams} />
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense>
      <SearchContent />
    </Suspense>
  );
}
