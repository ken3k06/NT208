type Props = {
  title: string;
  value: string;
  hint?: string;
  danger?: boolean;
};

export function StatCard({ title, value, hint, danger }: Props) {
  return (
    <div className="card kpi">
      <div style={{ color: "#9aa6c3", fontSize: 13 }}>{title}</div>
      <div style={{ fontSize: 28, marginTop: 6, color: danger ? "#ff5d73" : "#e8edf8" }}>{value}</div>
      {hint ? <div style={{ color: "#9aa6c3", fontSize: 13, marginTop: 8 }}>{hint}</div> : null}
    </div>
  );
}
