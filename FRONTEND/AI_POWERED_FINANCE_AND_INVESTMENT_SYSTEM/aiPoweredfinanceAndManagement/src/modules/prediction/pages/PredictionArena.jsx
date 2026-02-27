import { usePredictionEngine } from "../hooks/usePredictionEngine";
import AnimatedReveal from "../components/AnimatedReveal";
//update
import { submitPrediction } from "../prediction.api";
import ForecastCard from "../components/ForecastCard";
import MarketRealityChart from "../components/MarketRealityChart";
import ThoughtProcessPanel from "../components/ThoughtProcessPanel";
import ComparativeAnalysis from "../components/ComparativeAnalysis";
import ScoreCard from "../components/ScoreCard";

export default function PredictionArena() {
    const { data, loading } = usePredictionEngine();

    //   update for database
    const handleSubmit = async () => {
        const userData = {
            stock_symbol: "AAPL",
            predicted_direction: "up"
        };

        try {
            const result = await submitPrediction(userData);
            console.log("Backend Response:", result);
        } catch (error) {
            console.error(error);
        }
    };

    //end
    if (loading) {
        return (
            <div className="bg-slate-900 text-white min-h-screen flex items-center justify-center">
                <div className="animate-pulse text-xl">
                    AI is analyzing market signals...
                </div>
            </div>
        );
    }

    return (
        <div className="bg-slate-900 text-white min-h-screen p-6 space-y-6">

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

                <AnimatedReveal delay={0.2}>
                    <ForecastCard forecast={data.aiForecast} />
                </AnimatedReveal>

                <AnimatedReveal delay={0.4}>
                    <ThoughtProcessPanel indicators={data.indicators} />
                </AnimatedReveal>

                <AnimatedReveal delay={0.6}>
                    <MarketRealityChart reality={data.marketReality} />
                </AnimatedReveal>

                <AnimatedReveal delay={0.8}>
                    <ComparativeAnalysis comparison={data.comparison} />
                </AnimatedReveal>

            </div>

            <AnimatedReveal delay={1}>
                <ScoreCard scorecard={data.scorecard} />
            </AnimatedReveal>

            {/* update for backend */}
            <button
                onClick={handleSubmit}
                className="bg-blue-600 px-4 py-2 rounded"
            >
                Submit Prediction
            </button>

        </div>
    );
}