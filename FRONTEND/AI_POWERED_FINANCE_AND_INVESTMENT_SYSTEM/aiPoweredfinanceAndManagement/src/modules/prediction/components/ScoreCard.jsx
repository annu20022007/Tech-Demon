export default function ScoreCard({ scorecard }) {
  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg flex justify-around text-center">
      <div>
        <p className="text-gray-400">User Accuracy</p>
        <p className="text-green-400 text-2xl font-bold">
          {scorecard.userAccuracy}%
        </p>
      </div>
      <div>
        <p className="text-gray-400">AI Accuracy</p>
        <p className="text-cyan-400 text-2xl font-bold">
          {scorecard.aiAccuracy}%
        </p>
      </div>
    </div>
  );
}