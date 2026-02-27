export default function AIInsightCard({ insight }) {
  return (
    <div className="bg-blue-50 border border-blue-200 p-6 rounded-xl shadow-sm">
      <h3 className="font-semibold text-blue-800 mb-2">
        AI Portfolio Insight
      </h3>
      <p className="text-gray-700">{insight}</p>
    </div>
  );
}