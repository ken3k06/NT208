import Link from "next/link";

export default function HomePage() {
  return (
    <main className="container">
      <div className="card" style={{ padding: 24 }}>
        <h1 style={{ marginTop: 0 }}>CVHT Smart Advisor</h1>
        <p style={{ color: "#9aa6c3", marginBottom: 18 }}>
          Skeleton UI/UX cho hệ thống cố vấn học tập thông minh.
        </p>
        <Link
          href="/dashboard"
          style={{
            display: "inline-block",
            padding: "10px 14px",
            borderRadius: 10,
            background: "#4f8cff",
            color: "white",
            fontWeight: 600,
          }}
        >
          Mở Dashboard
        </Link>
      </div>
    </main>
  );
}
