import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";

export default function SentimentChart({ data }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h3 className="font-semibold mb-4">News Sentiment Impact</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="week" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="positive" fill="#22c55e" />
          <Bar dataKey="negative" fill="#ef4444" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}