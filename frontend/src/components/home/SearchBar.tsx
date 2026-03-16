'use client';

import { useState } from 'react';
import { useTranslations } from 'next-intl';
import { Search } from 'lucide-react';

export default function SearchBar() {
  const t = useTranslations('home');
  const [query, setQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: navigate to search results
    console.log('Search:', query);
  };

  return (
    <form onSubmit={handleSearch} className="flex w-full max-w-2xl mx-auto">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={t('search_placeholder')}
        className="flex-1 pl-5 pr-4 py-3 text-gray-900 rounded-l-full border-0 focus:outline-none focus:ring-2 focus:ring-indigo-300 text-base"
      />
      <button
        type="submit"
        className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-semibold px-6 py-3 rounded-r-full transition-colors flex items-center gap-2"
      >
        <Search className="h-5 w-5" />
        <span className="hidden sm:inline">Найти</span>
      </button>
    </form>
  );
}
