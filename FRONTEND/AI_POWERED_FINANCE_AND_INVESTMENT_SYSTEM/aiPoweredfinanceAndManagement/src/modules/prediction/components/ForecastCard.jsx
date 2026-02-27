export default function ForecastCard({ forecast }) {
  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-cyan-500">
      <h2 className="text-cyan-400 font-semibold mb-4">
        AI Forecast Card
      </h2>

      <p className="text-lg">
        ML predicts price to <span className="text-green-400">
          ${forecast.predictedPrice}
        </span>
      </p>

      <div className="mt-4">
        Confidence Score:
        <span className="text-cyan-300 ml-2 font-bold">
          {forecast.confidence}%
        </span>
      </div>
    </div>
  );
}