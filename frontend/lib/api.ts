const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function getMacroDashboard() {
  try {
    const res = await fetch(`${API_BASE}/dashboard/macro`, { cache: "no-store" });
    if (!res.ok) throw new Error("API error");
    return (await res.json()) as {
      faculty_avg_gpa: number;
      on_time_grad_rate: number;
      high_risk_students: number;
    };
  } catch {
    return {
      faculty_avg_gpa: 7.15,
      on_time_grad_rate: 0.74,
      high_risk_students: 42,
    };
  }
}

export async function uploadScoresCsv(file: File, accessToken: string) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/scores/upload-csv`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail ?? "Upload failed");
  }

  return (await res.json()) as {
    message: string;
    created: number;
    updated: number;
    skipped: number;
    scores_total: number;
  };
}
