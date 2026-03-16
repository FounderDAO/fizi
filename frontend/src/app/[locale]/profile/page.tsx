'use client';

import { useEffect, useState } from 'react';
import { useLocale } from 'next-intl';
import { useRouter } from 'next/navigation';
import { Settings, LogOut, Package, Heart } from 'lucide-react';
import api from '@/lib/api';
import ListingGrid from '@/components/listings/ListingGrid';

export default function ProfilePage() {
  const [user, setUser] = useState<any>(null);
  const [tab, setTab] = useState<'listings' | 'favorites'>('listings');
  const locale = useLocale();
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) { router.push(`/${locale}/login`); return; }
    api.get('/auth/profile/').then(res => setUser(res.data)).catch(() => {
      router.push(`/${locale}/login`);
    });
  }, []);

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push(`/${locale}`);
  };

  if (!user) return (
    <div className="max-w-3xl mx-auto px-4 py-16 text-center">
      <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full mx-auto" />
    </div>
  );

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="bg-white rounded-2xl border p-6 flex items-center gap-4 mb-6">
        <div className="w-16 h-16 rounded-full bg-indigo-100 flex items-center justify-center text-2xl font-bold text-indigo-600">
          {user.name?.[0]?.toUpperCase() || '?'}
        </div>
        <div className="flex-1">
          <h1 className="text-xl font-bold">{user.name || 'Без имени'}</h1>
          <p className="text-gray-500">{user.phone}</p>
          {user.is_verified && <span className="text-green-600 text-sm">✅ Верифицирован</span>}
        </div>
        <div className="flex gap-2">
          <button onClick={logout} className="p-2 text-gray-400 hover:text-red-500">
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        <button onClick={() => setTab('listings')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl font-medium ${tab === 'listings' ? 'bg-indigo-600 text-white' : 'bg-white border text-gray-600'}`}>
          <Package className="w-4 h-4" /> Мои объявления
        </button>
        <button onClick={() => setTab('favorites')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl font-medium ${tab === 'favorites' ? 'bg-indigo-600 text-white' : 'bg-white border text-gray-600'}`}>
          <Heart className="w-4 h-4" /> Избранное
        </button>
      </div>

      {tab === 'listings' && <ListingGrid endpoint="/listings/my/" />}
      {tab === 'favorites' && <ListingGrid endpoint="/listings/favorites/" />}
    </div>
  );
}
