import Link from 'next/link';
import { useLocale } from 'next-intl';
import { Heart, Eye, MapPin } from 'lucide-react';

interface ListingCardProps {
  id: number;
  title: string;
  price: number;
  currency: string;
  city: string;
  condition: string;
  cover_photo?: string;
  views: number;
  created_at: string;
  is_promoted?: boolean;
}

export default function ListingCard({
  id,
  title,
  price,
  currency,
  city,
  condition,
  cover_photo,
  views,
  is_promoted,
}: ListingCardProps) {
  const locale = useLocale();

  const formatPrice = (price: number, currency: string) => {
    if (currency === 'UZS') {
      return new Intl.NumberFormat('ru-RU').format(price) + ' сум';
    }
    return '$' + new Intl.NumberFormat('en-US').format(price);
  };

  return (
    <Link href={`/${locale}/listings/${id}`}>
      <div className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow border border-gray-100 cursor-pointer">
        {/* Photo */}
        <div className="relative h-48 bg-gray-100">
          {cover_photo ? (
            <img src={cover_photo} alt={title} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-gray-300 text-4xl">
              📷
            </div>
          )}
          {is_promoted && (
            <span className="absolute top-2 left-2 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-full">
              VIP
            </span>
          )}
          <button className="absolute top-2 right-2 bg-white/80 rounded-full p-1.5 hover:bg-white">
            <Heart className="w-4 h-4 text-gray-500" />
          </button>
        </div>
        {/* Info */}
        <div className="p-3">
          <p className="font-bold text-gray-900 text-lg">{formatPrice(price, currency)}</p>
          <p className="text-gray-700 text-sm mt-1 line-clamp-2">{title}</p>
          <div className="flex items-center justify-between mt-2 text-xs text-gray-400">
            <div className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              <span>{city}</span>
            </div>
            <div className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              <span>{views}</span>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
