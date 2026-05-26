"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { useState } from "react";
import { Movie } from "@/types";

interface Props {
  movie: Movie;
  onAddWatchlist?: (movie: Movie) => void;
}

export default function MovieCard({ movie, onAddWatchlist }: Props) {
  const [hovered, setHovered] = useState(false);
  const posterUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : null;

  return (
    <Link href={`/movie/${movie.movie_id}`}>
      <motion.div
        variants={{
          hidden: { opacity: 0, y: 24 },
          visible: {
            opacity: 1,
            y: 0,
            transition: { type: "spring", stiffness: 70 },
          },
        }}
        whileHover={{ scale: 1.04, y: -6 }}
        onHoverStart={() => setHovered(true)}
        onHoverEnd={() => setHovered(false)}
        className="relative rounded-xl overflow-hidden cursor-pointer bg-zinc-900 border border-zinc-800 hover:border-red-600 transition-colors duration-300 aspect-[2/3] shadow-2xl"
      >
        {posterUrl ? (
          <img
            src={posterUrl}
            alt={movie.title}
            className="absolute inset-0 w-full h-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="absolute inset-0 bg-zinc-800 flex items-center justify-center">
            <span className="text-zinc-600 text-xs font-mono">NO POSTER</span>
          </div>
        )}

        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/30 to-transparent" />

        <div className="absolute bottom-0 left-0 right-0 p-3 z-10">
          <h3 className="font-bold text-white text-sm leading-tight line-clamp-2">
            {movie.title}
          </h3>

          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: hovered ? 1 : 0, height: hovered ? "auto" : 0 }}
            transition={{ duration: 0.2 }}
            className="mt-2 space-y-1 overflow-hidden"
          >
            <div className="flex items-center justify-between">
              <span className="text-green-400 text-xs font-semibold">
                ★ {movie.vote_average.toFixed(1)}
              </span>
              {movie.confidence_score !== undefined && (
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-red-600/20 text-red-400 border border-red-500/30">
                  {Math.round(movie.confidence_score * 100)}% match
                </span>
              )}
            </div>
            {onAddWatchlist && (
              <button
                onClick={(e) => {
                  e.preventDefault();
                  e.stopPropagation();
                  onAddWatchlist(movie);
                }}
                className="w-full text-xs bg-white/10 hover:bg-white/20 text-white rounded py-1 transition"
              >
                + Watchlist
              </button>
            )}
          </motion.div>
        </div>
      </motion.div>
    </Link>
  );
}
