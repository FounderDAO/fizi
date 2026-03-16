'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useLocale } from 'next-intl';
import { Heart, Eye, MapPin, Phone, MessageCircle, Share2, ChevronLeft, ChevronRight } from 'lucide-react';
import api from '@/lib/api';
import Link from 'next/link';

export default function ListingDetailPage() {
  const { id, locale } = useParams() as { id: string; locale: string };
  const [listing, setListing] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [currentPhoto, setCurrentPhoto] = useState(0);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    api.get(`/listings/${id}/`).then(res => {
      setListing(res.data);
      setIsFavorite(res.data.is_favorite);
    }).finally(() => setLoading(false));
  }, [id]);

  const toggleFavorite = async () => {
    try {
      const res = await api.post(`/listings/${id}/favorite/`);
      setIsFavorite(res.data.favorited);
    } catch {
      // redirect to login if not auth
    }
  };

  const formatPrice = (price: number, currency: string) => {
    if (currency === 'UZS') return new Intl.NumberFormat('ru-RU').format(price) + ' сум';
    return '$' + new Intl.NumberFormat('en-US').format(price);
  };

  if (loading) return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="animate-pulse space-y-4">
        <div className="h-80 bg-gray-200 rounded-xl" />
        <div className="h-8 bg-gray-200 rounded w-1/2" />
        <div className="h-6 bg-gray-200 rounded w-1/4" />
      </div>
    </div>
  );

  if (!listing) return <div className="text-center py-20 text-gray-500">Объявление не найдено</div>;

  const photos = listing.photos || [];

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Back */}
      <Link href={`/${locale}`} className="flex items-center gap-1 text-gray-500 hover:text-gray-800 mb-4">
        <ChevronLeft className="w-4 h-4" /> Назад
      </Link>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Photos */}
        <div>
          <div className="relative h-80 bg-gray-100 rounded-2xl overflow-hidden">
            {photos.length > 0 ? (
              <img src={photos[currentPhoto]?.image} alt={listing.title}
                className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-6xl">📷</div>
            )}
            {photos.length > 1 && (
              <>
                <button onClick={() => setCurrentPhoto(p => Math.max(0, p - 1))}
                  className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2">
                  <ChevronLeft className="w-5 h-5" />
                </button>
                <button onClick={() => setCurrentPhoto(p => Math.min(photos.length - 1, p + 1))}
                  className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2">
                  <ChevronRight className="w-5 h-5" />
                </button>
              </>
            )}
          </div>
          {/* Thumbnails */}
          {photos.length > 1 && (
            <div className="flex gap-2 mt-3 overflow-x-auto">
              {photos.map((p: any, i: number) => (
                <img key={i} src={p.image} onClick={() => setCurrentPhoto(i)}
                  className={`w-16 h-16 object-cover rounded-lg cursor-pointer border-2 ${i === currentPhoto ? 'border-indigo-600' : 'border-transparent'}`} />
              ))}
            </div>
          )}
        </div>

        {/* Info */}
        <div className="space-y-4">
          <h1 className="text-2xl font-bold text-gray-900">{listing.title}</h1>
          <p className="text-3xl font-bold text-indigo-600">{formatPrice(listing.price, listing.currency)}</p>

          <div className="flex items-center gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-1">
              <MapPin className="w-4 h-4" /> {listing.city}
            </div>
            <div className="flex items-center gap-1">
              <Eye className="w-4 h-4" /> {listing.views} просмотров
            </div>
          </div>

          <div className="flex gap-2">
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${listing.condition === 'new' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'}`}>
              {listing.condition === 'new' ? 'Новое' : 'Б/у'}
            </span>
            {listing.category && (
              <span className="px-3 py-1 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700">
                {listing.category.name_ru}
              </span>
            )}
          </div>

          {/* Actions */}
          <div className="space-y-3 pt-2">
            <button className="w-full bg-indigo-600 text-white rounded-xl py-3 font-semibold flex items-center justify-center gap-2 hover:bg-indigo-700">
              <MessageCircle className="w-5 h-5" /> Написать продавцу
            </button>
            <button onClick={toggleFavorite}
              className={`w-full border rounded-xl py-3 font-semibold flex items-center justify-center gap-2 ${isFavorite ? 'border-red-400 text-red-500' : 'border-gray-300 text-gray-600 hover:border-gray-400'}`}>
              <Heart className={`w-5 h-5 ${isFavorite ? 'fill-red-500' : ''}`} />
              {isFavorite ? 'В избранном' : 'В избранное'}
            </button>
          </div>

          {/* Seller */}
          {listing.author && (
            <div className="border rounded-xl p-4 flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-xl">
                {listing.author.name?.[0] || '👤'}
              </div>
              <div>
                <p className="font-semibold">{listing.author.name || 'Пользователь'}</p>
                <div className="flex items-center gap-1">
                  <span className="text-yellow-500 text-sm">★ {listing.author.rating || '0.0'}</span>
                  {listing.author.is_verified && <span className="text-green-500 text-xs">✅ Верифицирован</span>}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Description */}
      <div className="mt-8 bg-white rounded-xl border p-6">
        <h2 className="text-lg font-bold mb-3">Описание</h2>
        <p className="text-gray-700 whitespace-pre-wrap">{listing.description}</p>
      </div>
    </div>
  );
}
