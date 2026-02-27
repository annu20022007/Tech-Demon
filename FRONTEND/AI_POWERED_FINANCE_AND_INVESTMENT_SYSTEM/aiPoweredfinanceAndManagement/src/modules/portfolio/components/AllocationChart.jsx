import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#ef4444"];

export default function AllocationChart({ portfolio }) {
  const chartData = portfolio.map((stock) => ({
    name: stock.symbol,
    value: stock.shares * stock.currentPrice,
  }));

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h3 className="mb-4 font-semibold">Allocation</h3>

      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            innerRadius={60}
            outerRadius={90}
          >
            {chartData.map((_, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}