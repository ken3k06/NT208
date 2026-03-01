import { StatCard } from "../../components/stat-card";
import { getMacroDashboard } from "../../lib/api";

export default async function DashboardPage() {
  const data = await getMacroDashboard();

  return (
    <main className="container">
      <h1 style={{ marginTop: 6 }}>Dean Dashboard (Macro)</h1>
      <p style={{ color: "#9aa6c3", marginTop: 4 }}>Theo dõi chất lượng đào tạo toàn khoa theo thời gian thực.</p>

      <section className="grid" style={{ marginTop: 18 }}>
        <StatCard title="GPA trung bình toàn khoa" value={data.faculty_avg_gpa.toFixed(2)} hint="Mục tiêu >= 7.0" />
        <StatCard
          title="Tỉ lệ tốt nghiệp đúng hạn"
          value={`${(data.on_time_grad_rate * 100).toFixed(1)}%`}
          hint="Dựa trên tốc độ tích lũy tín chỉ"
        />
        <StatCard
          title="Sinh viên rủi ro cao"
          value={`${data.high_risk_students}`}
          hint="Yêu cầu CVHT can thiệp"
          danger
        />
      </section>

      <section className="card" style={{ marginTop: 16 }}>
        <h3 style={{ marginTop: 0 }}>Roadmap UI/UX tiếp theo</h3>
        <ul style={{ color: "#c4cee6", lineHeight: 1.7, marginBottom: 0 }}>
          <li>Radar phổ điểm từng môn</li>
          <li>Leaderboard GPA giữa các lớp cùng khóa</li>
          <li>Risk Matrix 4 vùng: tín chỉ/GPA</li>
          <li>Chat AI truy vấn dữ liệu tiếng Việt</li>
        </ul>
      </section>
    </main>
  );
}
