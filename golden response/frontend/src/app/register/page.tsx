"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { useAuth } from "@/hooks/useAuth";

export default function RegisterPage() {
  const { signUp } = useAuth();
  const router = useRouter();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await signUp(name, email, password);
      router.push("/");
    } catch {
      setError("Registration failed. Email may already be in use.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0d0d0d] flex items-center justify-center px-4 pt-16">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-zinc-900 border border-zinc-800 rounded-xl p-8 space-y-4"
      >
        <h1 className="text-2xl font-bold">Create Account</h1>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="w-full px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-lg outline-none focus:border-red-600"
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-lg outline-none focus:border-red-600"
        />
        <input
          type="password"
          placeholder="Password (min 6 chars)"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={6}
          className="w-full px-4 py-3 bg-zinc-800 border border-zinc-700 rounded-lg outline-none focus:border-red-600"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-red-600 hover:bg-red-700 py-3 rounded-lg font-bold transition disabled:opacity-50"
        >
          {loading ? "Creating..." : "Sign Up"}
        </button>
        <p className="text-sm text-zinc-500 text-center">
          Already have an account?{" "}
          <Link href="/login" className="text-red-500 hover:underline">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}
