import Link from "next/link";

export default function HomePage() {
  return (
    <main className="container">
      <div className="card" style={{ padding: 24 }}>
        <h1 style={{ marginTop: 0 }}>CVHT Smart Advisor</h1>
        <p style={{ color: "#9aa6c3", marginBottom: 18 }}>
          Skeleton UI/UX cho hệ thống cố vấn học tập thông minh.
        </p>

        <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
          <Link
            href="/login"
            style={{
              display: "inline-block",
              padding: "10px 14px",
              borderRadius: 10,
              background: "#4f8cff",
              color: "white",
              fontWeight: 600,
            }}
          >
            Đăng nhập
          </Link>

          <Link
            href="/dashboard"
            style={{
              display: "inline-block",
              padding: "10px 14px",
              borderRadius: 10,
              background: "#1f2a44",
              color: "#dbe7ff",
              fontWeight: 600,
              border: "1px solid #334466",
            }}
          >
            Mở Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}
