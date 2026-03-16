'use client';

import { useEffect, useState } from 'react';
import ListingCard from './ListingCard';
import api from '@/lib/api';

interface Props {
  filters?: Record<string, string>;
  endpoint?: string;
}

export default function ListingGrid({ filters = {}, endpoint = '/listings/' }: Props) {
  const [listings, setListings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [count, setCount] = useState(0);

  useEffect(() => {
    const params = new URLSearchParams(filters as any);
    api.get(`${endpoint}?${params}`).then(res => {
      setListings(res.data.results || res.data);
      setCount(res.data.count || 0);
    }).catch(() => setListings([])).finally(() => setLoading(false));
  }, [JSON.stringify(filters), endpoint]);

  if (loading) return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {Array(8).fill(0).map((_, i) => (
        <div key={i} className="bg-white rounded-xl h-64 animate-pulse border" />
      ))}
    </div>
  );

  if (listings.length === 0) return (
    <div className="text-center py-16 text-gray-400">
      <div className="text-4xl mb-3">🔍</div>
      <p>Объявлений не найдено</p>
    </div>
  );

  return (
    <div>
      {count > 0 && <p className="text-gray-500 text-sm mb-4">{count} объявлений</p>}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {listings.map(listing => (
          <ListingCard key={listing.id} {...listing} />
        ))}
      </div>
    </div>
  );
}
