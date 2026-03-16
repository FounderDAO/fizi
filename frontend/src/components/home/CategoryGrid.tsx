'use client';

import { useEffect, useState } from 'react';
import { useLocale } from 'next-intl';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

export default function CategoryGrid() {
  const [categories, setCategories] = useState<any[]>([]);
  const locale = useLocale();
  const router = useRouter();

  useEffect(() => {
    api.get('/categories/').then(res => setCategories(res.data.slice(0, 12)));
  }, []);

  return (
    <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
      {categories.map((cat: any) => (
        <button key={cat.id}
          onClick={() => router.push(`/${locale}/search?category=${cat.slug}`)}
          className="flex flex-col items-center gap-2 p-3 bg-white rounded-xl border hover:border-indigo-400 hover:shadow-sm transition-all">
          <span className="text-3xl">{cat.icon}</span>
          <span className="text-xs text-center text-gray-700 font-medium leading-tight">{cat.name_ru}</span>
        </button>
      ))}
    </div>
  );
}
