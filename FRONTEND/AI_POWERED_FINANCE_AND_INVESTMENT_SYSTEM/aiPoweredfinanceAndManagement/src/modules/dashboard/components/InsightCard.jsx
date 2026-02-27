export default function InsightCard({ text }) {
  return (
    <div className="bg-blue-50 border border-blue-200 p-6 rounded-xl shadow-sm">
      <h3 className="font-semibold text-blue-800 mb-2">
        AI Insight of the Day
      </h3>
      <p className="text-gray-700">{text}</p>
    </div>
  );
}