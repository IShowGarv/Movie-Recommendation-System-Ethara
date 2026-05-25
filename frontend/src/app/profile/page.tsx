"use client";

import ProtectedRoute from "@/components/ProtectedRoute";
import { useAuth } from "@/hooks/useAuth";

function ProfileContent() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white pt-24 px-10">
      <h1 className="text-3xl font-bold mb-6">Profile</h1>
      <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 max-w-md space-y-2">
        <p>
          <span className="text-zinc-500">Name:</span> {user?.name}
        </p>
        <p>
          <span className="text-zinc-500">Email:</span> {user?.email}
        </p>
      </div>
    </div>
  );
}

export default function ProfilePage() {
  return (
    <ProtectedRoute>
      <ProfileContent />
    </ProtectedRoute>
  );
}
