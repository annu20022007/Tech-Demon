import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";

export default function MarketRealityChart({ reality }) {
  // Mock historical trend data
  const data = [
    { time: "10AM", price: 246 },
    { time: "11AM", price: 247 },
    { time: "12PM", price: 249 },
    { time: "1PM", price: 248 },
    { time: "2PM", price: 250 },
    { time: "3PM", price: reality.actualPrice },
  ];

  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
      <h2 className="text-green-400 font-semibold mb-6">
        Market Reality vs Forecast
      </h2>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="time" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1e293b",
                border: "1px solid #334155",
                color: "#fff",
              }}
            />
            <Legend />

            {/* Actual Market Line */}
            <Line
              type="monotone"
              dataKey="price"
              stroke="#22c55e"
              strokeWidth={3}
              dot={{ r: 4 }}
              name="Actual Price"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 text-sm text-gray-400">
        Final Market Close:{" "}
        <span className="text-green-400 font-semibold">
          ${reality.actualPrice}
        </span>
      </div>
    </div>
  );
}