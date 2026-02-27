export default function RiskMeter({ portfolio }) {
  const total = portfolio.reduce(
    (sum, s) => sum + s.shares * s.currentPrice,
    0
  );

  const maxStock = Math.max(
    ...portfolio.map((s) => s.shares * s.currentPrice)
  );

  const concentration = (maxStock / total) * 100;

  let risk = "Low";
  if (concentration > 60) risk = "High";
  else if (concentration > 40) risk = "Medium";

  return (
    <div className="bg-white p-6 rounded-xl shadow-md">
      <h3 className="font-semibold mb-2">Risk Level</h3>
      <p className="text-xl font-bold">{risk}</p>
      <p className="text-sm text-gray-500">
        Largest holding: {concentration.toFixed(1)}%
      </p>
    </div>
  );
}