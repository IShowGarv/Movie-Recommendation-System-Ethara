"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import ProtectedRoute from "@/components/ProtectedRoute";
import { getWatchlist, removeFromWatchlist } from "@/services/api";
import { WatchlistItem } from "@/types";

function WatchlistContent() {
  const [items, setItems] = useState<WatchlistItem[]>([]);
  const [loading, setLoading] = useState(true);

  const load = () => {
    getWatchlist()
      .then((res) => setItems(res.data.watchlist || []))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  const handleRemove = async (movieId: number) => {
    await removeFromWatchlist(movieId);
    setItems((prev) => prev.filter((i) => i.movie_id !== movieId));
  };

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white pt-24 px-10">
      <h1 className="text-3xl font-bold mb-8">My Watchlist</h1>
      {loading ? (
        <p className="text-zinc-500">Loading...</p>
      ) : items.length === 0 ? (
        <p className="text-zinc-500">
          Your watchlist is empty.{" "}
          <Link href="/search" className="text-red-500 hover:underline">
            Search movies
          </Link>
        </p>
      ) : (
        <ul className="space-y-3 max-w-lg">
          {items.map((item) => (
            <li
              key={item.movie_id}
              className="flex items-center justify-between bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3"
            >
              <Link
                href={`/movie/${item.movie_id}`}
                className="font-medium hover:text-red-400 transition"
              >
                {item.title}
              </Link>
              <button
                onClick={() => handleRemove(item.movie_id)}
                className="text-xs text-zinc-400 hover:text-red-500 transition"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function WatchlistPage() {
  return (
    <ProtectedRoute>
      <WatchlistContent />
    </ProtectedRoute>
  );
}
