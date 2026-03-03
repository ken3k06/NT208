"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { FormEvent, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState("admin@uit.edu.vn");
  const [password, setPassword] = useState("admin123");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Sai email hoặc mật khẩu");
      }

      const data = (await res.json()) as { access_token: string; role: string };
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("user_role", data.role);
      document.cookie = `access_token=${encodeURIComponent(data.access_token)}; Path=/; Max-Age=${60 * 60 * 24 * 7}; SameSite=Lax`;
      document.cookie = `user_role=${encodeURIComponent(data.role)}; Path=/; Max-Age=${60 * 60 * 24 * 7}; SameSite=Lax`;
      const nextPath = searchParams.get("next");
      router.push(nextPath && nextPath.startsWith("/") ? nextPath : "/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Đăng nhập thất bại");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container" style={{ maxWidth: 560 }}>
      <div className="card" style={{ padding: 24 }}>
        <h1 style={{ marginTop: 0, marginBottom: 8 }}>Đăng nhập</h1>
        <p style={{ color: "#9aa6c3", marginTop: 0, marginBottom: 18 }}>
          Dùng tài khoản demo để test UI/UX và API.
        </p>

        <form onSubmit={onSubmit} style={{ display: "grid", gap: 12 }}>
          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ color: "#c7d5f2" }}>Email</span>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              type="email"
              required
              style={{
                padding: "10px 12px",
                borderRadius: 10,
                border: "1px solid #2c3a57",
                background: "#0f1628",
                color: "#e8edf8",
              }}
            />
          </label>

          <label style={{ display: "grid", gap: 6 }}>
            <span style={{ color: "#c7d5f2" }}>Mật khẩu</span>
            <input
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              required
              style={{
                padding: "10px 12px",
                borderRadius: 10,
                border: "1px solid #2c3a57",
                background: "#0f1628",
                color: "#e8edf8",
              }}
            />
          </label>

          {error && (
            <p style={{ margin: 0, color: "#ff7e92", fontSize: 14 }}>
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              marginTop: 4,
              padding: "11px 14px",
              borderRadius: 10,
              border: "none",
              background: "#4f8cff",
              color: "#fff",
              fontWeight: 700,
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? "Đang đăng nhập..." : "Đăng nhập"}
          </button>
        </form>

        <p style={{ marginTop: 16, marginBottom: 0, color: "#9aa6c3", fontSize: 14 }}>
          Demo: admin@uit.edu.vn / admin123 hoặc advisor1@uit.edu.vn / advisor123
        </p>

        <div style={{ marginTop: 16 }}>
          <Link href="/" style={{ color: "#9ec0ff" }}>
            ← Quay về trang chủ
          </Link>
        </div>
      </div>
    </main>
  );
}
