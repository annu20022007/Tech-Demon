import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function PerformanceChart({ history }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h3 className="font-semibold mb-4">
        Historical Performance
      </h3>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={history}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#2563eb"
            strokeWidth={3}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}