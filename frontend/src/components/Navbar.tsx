"use client";

import Link from "next/link";
import { useAuth } from "@/hooks/useAuth";

export default function Navbar() {
  const { isAuthenticated, user, signOut } = useAuth();

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-b from-black/90 to-transparent px-6 py-4 flex items-center justify-between">
      <Link href="/" className="text-red-600 font-black text-2xl tracking-tighter">
        CINEMA<span className="text-white">AI</span>
      </Link>
      <div className="flex items-center gap-6 text-sm font-medium">
        <Link href="/" className="text-gray-300 hover:text-white transition">
          Home
        </Link>
        <Link href="/search" className="text-gray-300 hover:text-white transition">
          Search
        </Link>
        {isAuthenticated && (
          <Link
            href="/watchlist"
            className="text-gray-300 hover:text-white transition"
          >
            Watchlist
          </Link>
        )}
        {isAuthenticated ? (
          <>
            <Link
              href="/profile"
              className="text-gray-300 hover:text-white transition"
            >
              {user?.name || "Profile"}
            </Link>
            <button
              onClick={signOut}
              className="text-gray-400 hover:text-white transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="text-gray-300 hover:text-white transition">
              Login
            </Link>
            <Link
              href="/register"
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-1.5 rounded transition"
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
