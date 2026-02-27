import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const COLORS = ["#2563eb", "#16a34a", "#f59e0b", "#ef4444"];

export default function SectorChart({ portfolio }) {
  const sectorData = {};

  portfolio.forEach((stock) => {
    const value = stock.shares * stock.currentPrice;
    sectorData[stock.sector] =
      (sectorData[stock.sector] || 0) + value;
  });

  const formatted = Object.entries(sectorData).map(
    ([sector, value]) => ({ name: sector, value })
  );

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h3 className="font-semibold mb-4">Sector Allocation</h3>

      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie data={formatted} dataKey="value" innerRadius={60}>
            {formatted.map((_, index) => (
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