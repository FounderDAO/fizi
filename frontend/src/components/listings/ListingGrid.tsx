'use client';

import { useEffect, useState } from 'react';
import ListingCard from './ListingCard';
import api from '@/lib/api';

export default function ListingGrid({
  query = '',
  categorySlug = '',
}: {
  query?: string;
  categorySlug?: string;
}) {
  const [listings, setListings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (categorySlug) params.set('category', categorySlug);

    api
      .get(`/listings/?${params}`)
      .then((res) => {
        setListings(res.data.results || []);
      })
      .finally(() => setLoading(false));
  }, [query, categorySlug]);

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {Array(8)
          .fill(0)
          .map((_, i) => (
            <div key={i} className="bg-white rounded-xl h-64 animate-pulse" />
          ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {listings.map((listing) => (
        <ListingCard key={listing.id} {...listing} />
      ))}
    </div>
  );
}
