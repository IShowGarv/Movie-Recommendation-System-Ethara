"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import {
  addToWatchlist,
  getMovie,
  getRecommendations,
} from "@/services/api";
import { useAuth } from "@/hooks/useAuth";
import { Movie } from "@/types";
import MovieRow from "@/components/MovieRow";

export default function MovieDetailPage() {
  const params = useParams();
  const movieId = Number(params.id);
  const { isAuthenticated } = useAuth();
  const [movie, setMovie] = useState<Movie | null>(null);
  const [recommendations, setRecommendations] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!movieId || Number.isNaN(movieId)) return;
    setLoading(true);
    Promise.all([
      getMovie(movieId),
      getRecommendations(movieId, 12),
    ])
      .then(([movieRes, recoRes]) => {
        setMovie(movieRes.data);
        setRecommendations(recoRes.data);
      })
      .catch(() => {
        setMovie(null);
        setRecommendations([]);
      })
      .finally(() => setLoading(false));
  }, [movieId]);

  const handleWatchlist = async () => {
    if (!movie || !isAuthenticated) {
      setMessage("Please log in to add to watchlist.");
      return;
    }
    try {
      await addToWatchlist(movie.movie_id, movie.title);
      setMessage(`Added "${movie.title}" to watchlist.`);
    } catch {
      setMessage("Could not add to watchlist.");
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0d0d0d] pt-24 flex items-center justify-center text-zinc-500">
        Loading...
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="min-h-screen bg-[#0d0d0d] pt-24 flex items-center justify-center text-zinc-500">
        Movie not found.
      </div>
    );
  }

  const posterUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w780${movie.poster_path}`
    : null;

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white pt-20">
      <div className="px-10 py-8 flex flex-col md:flex-row gap-8">
        <div className="w-full md:w-80 shrink-0">
          {posterUrl ? (
            <img
              src={posterUrl}
              alt={movie.title}
              className="rounded-xl w-full aspect-[2/3] object-cover border border-zinc-800"
            />
          ) : (
            <div className="rounded-xl aspect-[2/3] bg-zinc-800 flex items-center justify-center text-zinc-600">
              No poster
            </div>
          )}
        </div>
        <div className="flex-1 space-y-4">
          <h1 className="text-4xl font-black">{movie.title}</h1>
          <p className="text-green-400 font-semibold">
            ★ {movie.vote_average.toFixed(1)}
          </p>
          {movie.release_date && (
            <p className="text-zinc-400 text-sm">{movie.release_date}</p>
          )}
          <p className="text-gray-300 leading-relaxed">{movie.overview}</p>
          <button
            onClick={handleWatchlist}
            className="bg-red-600 hover:bg-red-700 px-6 py-2 rounded font-bold transition"
          >
            + Add to Watchlist
          </button>
          {message && <p className="text-sm text-zinc-400">{message}</p>}
        </div>
      </div>

      <MovieRow title="Because you viewed this" movies={recommendations} />
    </div>
  );
}
