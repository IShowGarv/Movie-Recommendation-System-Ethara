"use client";

import SearchBar from "@/components/SearchBar";

export default function SearchPage() {
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white pt-24 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">Search Movies</h1>
      <SearchBar />
    </div>
  );
}
