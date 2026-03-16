import Link from 'next/link';
import { MapPin, Eye } from 'lucide-react';

export interface ListingCardProps {
  id: string;
  title: string;
  price: number;
  currency?: string;
  city: string;
  date: string;
  imageUrl?: string;
  condition?: 'new' | 'used';
  views?: number;
}

export default function ListingCard({
  id,
  title,
  price,
  currency = 'сум',
  city,
  date,
  imageUrl,
  condition,
  views,
}: ListingCardProps) {
  const formattedPrice = new Intl.NumberFormat('ru-UZ').format(price);

  return (
    <Link href={`/ru/listings/${id}`} className="group">
      <div className="bg-white rounded-xl overflow-hidden border border-gray-100 hover:border-indigo-200 hover:shadow-lg transition-all">
        {/* Image */}
        <div className="aspect-[4/3] bg-gray-100 overflow-hidden relative">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-300">
              <svg className="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          )}
          {condition && (
            <span className={`absolute top-2 left-2 text-xs font-semibold px-2 py-0.5 rounded-full ${
              condition === 'new'
                ? 'bg-green-100 text-green-700'
                : 'bg-gray-100 text-gray-600'
            }`}>
              {condition === 'new' ? 'Новое' : 'Б/у'}
            </span>
          )}
        </div>

        {/* Info */}
        <div className="p-3">
          <p className="text-base font-bold text-indigo-600">
            {formattedPrice} <span className="text-xs font-normal text-gray-500">{currency}</span>
          </p>
          <p className="text-sm text-gray-800 mt-1 line-clamp-2 leading-snug">{title}</p>
          <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <MapPin className="h-3 w-3" />
              {city}
            </span>
            <span className="flex items-center gap-2">
              {views !== undefined && (
                <span className="flex items-center gap-0.5">
                  <Eye className="h-3 w-3" />
                  {views}
                </span>
              )}
              <span>{date}</span>
            </span>
          </div>
        </div>
      </div>
    </Link>
  );
}
