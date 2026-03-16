'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useTranslations } from 'next-intl';
import { Search, Heart, MessageCircle, User, PlusCircle } from 'lucide-react';

const locales = [
  { code: 'ru', label: 'RU' },
  { code: 'uz', label: 'UZ' },
  { code: 'en', label: 'EN' },
];

export default function Navbar() {
  const t = useTranslations('nav');
  const pathname = usePathname();
  const router = useRouter();

  const currentLocale = locales.find((l) => pathname.startsWith(`/${l.code}`))?.code || 'ru';

  const switchLocale = (locale: string) => {
    const segments = pathname.split('/');
    segments[1] = locale;
    router.push(segments.join('/'));
  };

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href={`/${currentLocale}`} className="flex items-center gap-2">
            <span className="text-2xl font-extrabold text-indigo-600 tracking-tight">
              Fizi
              <span className="text-gray-400 font-normal">.uz</span>
            </span>
          </Link>

          {/* Search bar (desktop) */}
          <div className="hidden md:flex flex-1 max-w-xl mx-8">
            <div className="relative w-full">
              <input
                type="text"
                placeholder={t('search')}
                className="w-full pl-4 pr-10 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <Search className="absolute right-3 top-2.5 h-4 w-4 text-gray-400" />
            </div>
          </div>

          {/* Nav links */}
          <div className="flex items-center gap-4">
            {/* Post ad button */}
            <Link
              href={`/${currentLocale}/create`}
              className="hidden md:flex items-center gap-1.5 bg-indigo-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-indigo-700 transition-colors"
            >
              <PlusCircle className="h-4 w-4" />
              {t('post')}
            </Link>

            {/* Icons */}
            <Link href={`/${currentLocale}/favorites`} className="text-gray-500 hover:text-indigo-600 transition-colors">
              <Heart className="h-5 w-5" />
            </Link>
            <Link href={`/${currentLocale}/messages`} className="text-gray-500 hover:text-indigo-600 transition-colors">
              <MessageCircle className="h-5 w-5" />
            </Link>
            <Link href={`/${currentLocale}/profile`} className="text-gray-500 hover:text-indigo-600 transition-colors">
              <User className="h-5 w-5" />
            </Link>

            {/* Login */}
            <Link
              href={`/${currentLocale}/login`}
              className="text-sm font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
            >
              {t('login')}
            </Link>

            {/* Language switcher */}
            <div className="flex items-center gap-1 border border-gray-200 rounded-full px-2 py-1">
              {locales.map((locale) => (
                <button
                  key={locale.code}
                  onClick={() => switchLocale(locale.code)}
                  className={`text-xs font-semibold px-1.5 py-0.5 rounded-full transition-colors ${
                    currentLocale === locale.code
                      ? 'bg-indigo-600 text-white'
                      : 'text-gray-500 hover:text-indigo-600'
                  }`}
                >
                  {locale.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
