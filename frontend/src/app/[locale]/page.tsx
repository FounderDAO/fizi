import { useTranslations } from 'next-intl';
import SearchBar from '@/components/home/SearchBar';
import CategoryGrid from '@/components/home/CategoryGrid';
import ListingGrid from '@/components/listings/ListingGrid';

export default function HomePage() {
  const t = useTranslations('home');

  return (
    <div>
      {/* Hero */}
      <div className="bg-indigo-600 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">{t('title')}</h1>
          <p className="text-indigo-200 text-lg mb-8">{t('subtitle')}</p>
          <SearchBar />
        </div>
      </div>

      {/* Categories */}
      <div className="max-w-7xl mx-auto px-4 py-10">
        <h2 className="text-2xl font-bold mb-6">{t('categories')}</h2>
        <CategoryGrid />
      </div>

      {/* Latest listings */}
      <div className="max-w-7xl mx-auto px-4 pb-16">
        <h2 className="text-2xl font-bold mb-6">{t('latest')}</h2>
        <ListingGrid />
      </div>
    </div>
  );
}
