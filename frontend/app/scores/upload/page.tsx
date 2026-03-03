"use client";

import Link from "next/link";
import { FormEvent, useMemo, useState } from "react";

import { uploadScoresCsv } from "../../../lib/api";

type UploadResult = {
  message: string;
  created: number;
  updated: number;
  skipped: number;
  scores_total: number;
};

export default function UploadScoresPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<UploadResult | null>(null);

  const token = useMemo(() => {
    if (typeof window === "undefined") return "";
    return localStorage.getItem("access_token") ?? "";
  }, []);

  const role = useMemo(() => {
    if (typeof window === "undefined") return "";
    return localStorage.getItem("user_role") ?? "";
  }, []);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!token) {
      setError("Bạn chưa đăng nhập. Vui lòng đăng nhập trước.");
      return;
    }

    if (!file) {
      setError("Bạn chưa chọn file CSV.");
      return;
    }

    setLoading(true);
    try {
      const res = await uploadScoresCsv(file, token);
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload thất bại");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container" style={{ maxWidth: 760 }}>
      <div className="card" style={{ padding: 24 }}>
        <h1 style={{ marginTop: 0, marginBottom: 8 }}>Upload CSV điểm</h1>
        <p style={{ color: "#9aa6c3", marginTop: 0 }}>
          Endpoint chỉ cho ADMIN. Format cột: student_code, semester, course_code, credits, total_score.
        </p>

        {!token && (
          <p style={{ color: "#ff7e92" }}>
            Chưa có phiên đăng nhập. Bấm <Link href="/login" style={{ color: "#9ec0ff" }}>đăng nhập</Link> trước.
          </p>
        )}

        {token && role !== "ADMIN" && (
          <p style={{ color: "#ffcf70" }}>
            Bạn đang đăng nhập role {role}. Chỉ role ADMIN mới upload được.
          </p>
        )}

        <form onSubmit={onSubmit} style={{ display: "grid", gap: 12, marginTop: 12 }}>
          <input
            type="file"
            accept=".csv,text/csv"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            style={{
              padding: "10px 12px",
              borderRadius: 10,
              border: "1px solid #2c3a57",
              background: "#0f1628",
              color: "#e8edf8",
            }}
          />

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "fit-content",
              padding: "10px 14px",
              borderRadius: 10,
              border: "none",
              background: "#4f8cff",
              color: "white",
              fontWeight: 700,
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? "Đang upload..." : "Upload và cập nhật điểm"}
          </button>
        </form>

        {error && <p style={{ color: "#ff7e92", marginBottom: 0 }}>{error}</p>}

        {result && (
          <div className="card" style={{ marginTop: 14 }}>
            <h3 style={{ marginTop: 0 }}>Kết quả import</h3>
            <p style={{ margin: "6px 0" }}>Created: {result.created}</p>
            <p style={{ margin: "6px 0" }}>Updated: {result.updated}</p>
            <p style={{ margin: "6px 0" }}>Skipped: {result.skipped}</p>
            <p style={{ margin: "6px 0 0" }}>Total scores: {result.scores_total}</p>
          </div>
        )}

        <div style={{ marginTop: 16, display: "flex", gap: 12, flexWrap: "wrap" }}>
          <Link href="/dashboard" style={{ color: "#9ec0ff" }}>
            ← Về Dashboard
          </Link>
          <Link href="/login" style={{ color: "#9ec0ff" }}>
            Đổi tài khoản
          </Link>
        </div>
      </div>
    </main>
  );
}
