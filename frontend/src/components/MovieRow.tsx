"use client";

import { motion } from "framer-motion";
import { Movie } from "@/types";
import MovieCard from "./MovieCard";
import SkeletonCard from "./SkeletonCard";

interface Props {
  title: string;
  movies: Movie[];
  loading?: boolean;
  onAddWatchlist?: (movie: Movie) => void;
}

export default function MovieRow({
  title,
  movies,
  loading,
  onAddWatchlist,
}: Props) {
  return (
    <section className="px-10 pb-10">
      <h2 className="text-xl font-semibold mb-5 text-gray-100 tracking-wide">
        {title}
      </h2>
      <motion.div
        initial="hidden"
        animate="visible"
        variants={{ visible: { transition: { staggerChildren: 0.06 } } }}
        className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4"
      >
        {loading
          ? [...Array(8)].map((_, i) => <SkeletonCard key={i} />)
          : movies.map((m) => (
              <MovieCard
                key={m.movie_id}
                movie={m}
                onAddWatchlist={onAddWatchlist}
              />
            ))}
      </motion.div>
    </section>
  );
}
