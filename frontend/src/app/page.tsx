"use client";

import { useEffect, useState } from "react";
import { getPopularMovies } from "@/services/api";
import { Movie } from "@/types";
import HeroBanner from "@/components/HeroBanner";
import MovieRow from "@/components/MovieRow";
import SearchBar from "@/components/SearchBar";

export default function HomePage() {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPopularMovies(16)
      .then((res) => setMovies(res.data))
      .catch(() => setMovies([]))
      .finally(() => setLoading(false));
  }, []);

  const hero = movies[0];

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white pt-16">
      {hero && <HeroBanner movie={hero} />}

      <div className="px-10 py-8">
        <SearchBar />
      </div>

      <MovieRow title="Popular Right Now" movies={movies} loading={loading} />
    </div>
  );
}
