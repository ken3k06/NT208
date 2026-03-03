"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

type AuthState = {
  token: string;
  role: string;
};

export function AuthNav() {
  const router = useRouter();
  const pathname = usePathname();
  const [auth, setAuth] = useState<AuthState>({ token: "", role: "" });

  useEffect(() => {
    const token = localStorage.getItem("access_token") ?? "";
    const role = localStorage.getItem("user_role") ?? "";
    setAuth({ token, role });
  }, [pathname]);

  function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");
    document.cookie = "access_token=; Path=/; Max-Age=0; SameSite=Lax";
    document.cookie = "user_role=; Path=/; Max-Age=0; SameSite=Lax";
    setAuth({ token: "", role: "" });
    router.push("/login");
  }

  return (
    <header className="container" style={{ paddingBottom: 0 }}>
      <div className="card" style={{ padding: "10px 14px", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
        <Link href="/" style={{ fontWeight: 700, color: "#dce8ff" }}>
          CVHT Smart Advisor
        </Link>

        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {auth.token ? (
            <>
              <span style={{ color: "#9aa6c3", fontSize: 13 }}>Role: {auth.role || "-"}</span>
              <button
                onClick={logout}
                style={{
                  border: "1px solid #3a4968",
                  background: "#1a243c",
                  color: "#e8edf8",
                  borderRadius: 10,
                  padding: "8px 12px",
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Đăng xuất
              </button>
            </>
          ) : (
            <Link
              href="/login"
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 10,
                background: "#4f8cff",
                color: "white",
                fontWeight: 600,
              }}
            >
              Đăng nhập
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
