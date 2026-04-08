import Link from "next/link";
import { API_BASE_URL } from "@/lib/api";

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
      <main className="w-full max-w-xl rounded-xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900">KASU Frontend</h1>
        <p className="mt-2 text-slate-600">
          Frontend Next.js connecte au backend Django.
        </p>

        <div className="mt-6 space-y-3">
          <p className="text-sm text-slate-700">
            API configuree sur: <span className="font-mono">{API_BASE_URL}</span>
          </p>

          <div className="flex gap-3">
            <Link
              href="/login"
              className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white"
            >
              Se connecter
            </Link>
            <Link
              href="/dashboard"
              className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-800"
            >
              Dashboard
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}
