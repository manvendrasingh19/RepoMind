
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from "recharts";

const languageData = [
  { name: "TypeScript", value: 42, color: "#3B82F6" },
  { name: "Python", value: 28, color: "#A78BFA" },
  { name: "JavaScript", value: 18, color: "#EAB308" },
  { name: "CSS", value: 7, color: "#06B6D4" },
  { name: "Other", value: 5, color: "#64748B" },
];

export default function LanguageChart() {
  return (
    <div className="panel">
      <div className="panel-heading">
        <div>
          <h3>Language distribution</h3>
          <p>Code composition across repositories</p>
        </div>

        <span className="panel-period">All repositories</span>
      </div>

      <div className="language-content">
        <div className="language-chart">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={languageData}
                dataKey="value"
                nameKey="name"
                innerRadius={65}
                outerRadius={91}
                paddingAngle={4}
                stroke="none"
              >
                {languageData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>

              <Tooltip
                contentStyle={{
                  background: "#18181b",
                  border: "1px solid #333",
                  borderRadius: "10px",
                  color: "#fff",
                }}
                formatter={(value) => [`${value}%`, "Share"]}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="language-legend">
          {languageData.map((item) => (
            <div className="legend-item" key={item.name}>
              <span
                className="legend-dot"
                style={{ background: item.color }}
              />
              <span className="legend-name">{item.name}</span>
              <strong>{item.value}%</strong>
            </div>
          ))}
        </div>
      </div>

      <div className="demo-notice">
        <span className="status-dot" />
        Illustrative demo data — live repository analysis coming soon
      </div>
    </div>
  );
}
