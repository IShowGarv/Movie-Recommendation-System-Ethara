"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Movie } from "@/types";

interface Props {
  movie: Movie;
}

export default function HeroBanner({ movie }: Props) {
  const posterUrl = movie.poster_path
    ? `https://image.tmdb.org/t/p/w1280${movie.poster_path}`
    : null;

  return (
    <div className="relative h-[75vh] flex items-end pb-16 px-10 pt-20">
      {posterUrl && (
        <img
          src={posterUrl}
          alt=""
          className="absolute inset-0 w-full h-full object-cover opacity-40"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-r from-black via-black/70 to-transparent z-10" />
      <div className="absolute inset-0 bg-zinc-900/30 z-10" />
      <div className="relative z-20 max-w-xl space-y-4">
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-red-500 uppercase tracking-widest text-xs font-bold"
        >
          AI Top Pick
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-5xl md:text-6xl font-black tracking-tight"
        >
          {movie.title}
        </motion.h1>
        <p className="text-gray-300 line-clamp-3 text-sm">{movie.overview}</p>
        <div className="flex gap-3 pt-1">
          <Link
            href={`/movie/${movie.movie_id}`}
            className="bg-white text-black px-6 py-2 rounded font-bold hover:bg-gray-200 transition"
          >
            ▶ More Info
          </Link>
        </div>
      </div>
    </div>
  );
}
