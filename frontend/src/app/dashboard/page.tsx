"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { API_BASE_URL, fetchWithAuth } from "@/lib/api";
import { clearTokens, getAccessToken } from "@/lib/auth";

export default function DashboardPage() {
  const router = useRouter();
  const [status, setStatus] = useState("Chargement...");

  useEffect(() => {
    const access = getAccessToken();
    if (!access) {
      router.replace("/login");
      return;
    }

    fetchWithAuth("/api/schema/", access)
      .then(async (response) => {
        if (!response.ok) {
          const body = await response.text();
          throw new Error(`${response.status} ${response.statusText} ${body}`);
        }
        setStatus("Connexion API OK");
      })
      .catch((error) => setStatus(`Erreur API: ${String(error)}`));
  }, [router]);

  function handleLogout() {
    clearTokens();
    router.push("/login");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
      <main className="w-full max-w-2xl rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard KASU</h1>
        <p className="mt-2 text-slate-700">Etat API: {status}</p>

        <div className="mt-6 space-y-2 rounded-md bg-slate-100 p-4 text-sm">
          <p>
            <span className="font-semibold">Base URL API:</span> {API_BASE_URL}
          </p>
          <p>
            <span className="font-semibold">Access token:</span> Present
          </p>
        </div>

        <div className="mt-6 flex gap-3">
          <Link
            href="/"
            className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-800"
          >
            Accueil
          </Link>
          <button
            type="button"
            onClick={handleLogout}
            className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white"
          >
            Deconnexion
          </button>
        </div>
      </main>
    </div>
  );
}
