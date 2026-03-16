'use client';
import { useLocale } from 'next-intl';
import { useRouter } from 'next/navigation';

interface Props {
  subcategories: any[];
  currentSlug?: string;
}

export default function SubcategoryList({ subcategories, currentSlug }: Props) {
  const locale = useLocale();
  const router = useRouter();

  if (!subcategories.length) return null;

  return (
    <div className="bg-white rounded-xl border p-4 mb-4">
      <h3 className="font-semibold text-sm text-gray-500 mb-3 uppercase tracking-wide">Подкатегории</h3>
      <div className="space-y-1">
        {subcategories.map((sub: any) => (
          <button key={sub.id}
            onClick={() => router.push(`/${locale}/search?category=${sub.slug}`)}
            className={`w-full text-left px-3 py-2 rounded-lg text-sm flex justify-between items-center hover:bg-gray-50 ${
              currentSlug === sub.slug ? 'bg-indigo-50 text-indigo-700 font-medium' : 'text-gray-700'
            }`}>
            <span>{sub.icon} {sub.name_ru}</span>
            <span className="text-gray-400 text-xs">{sub.listing_count?.toLocaleString()}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
