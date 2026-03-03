import "./globals.css";
import type { Metadata } from "next";
import type { ReactNode } from "react";

import { AuthNav } from "../components/auth-nav";

export const metadata: Metadata = {
  title: "CVHT Smart Advisor",
  description: "Advising analytics dashboard",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="vi">
      <body>
        <AuthNav />
        {children}
      </body>
    </html>
  );
}
