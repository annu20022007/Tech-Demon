import { apiFetch } from "../../services/api";

const USE_BACKEND = true; // ✅ Backend enabled

/*
 * Fetch AI prediction data for a given symbol
 */
export const fetchPredictionData = async (symbol = "AAPL") => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/prediction/analyze", {
        method: "GET",
      });
    } catch (error) {
      console.error("Prediction fetch error:", error);
      // Fallback to mock data if backend fails
      return getMockPrediction();
    }
  }
  return getMockPrediction();
};

/*
 * Submit user prediction
 */
export const submitPrediction = async (data) => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/prediction/submit", {
        method: "POST",
        body: JSON.stringify(data),
      });
    } catch (error) {
      console.error("Prediction submit error:", error);
      throw error;
    }
  }
  throw new Error("Backend disabled");
};

/*
 * Mock prediction data (fallback when backend is unavailable)
 */
function getMockPrediction() {
  return {
    aiForecast: {
      direction: "up",
      confidence: 0.75,
      predictedPrice: 185
    },
    indicators: {
      rsi: 58,
      macd: "bullish crossover",
      movingAverage: "above 200 EMA"
    },
    marketReality: {
      actualPrice: 178,
      volume: 32000000
    },
    comparison: {
      userPrediction: "up",
      aiPrediction: "up",
      accuracy: "Correct"
    },
    scorecard: {
      totalPredictions: 10,
      correctPredictions: 7,
      winRate: "70%"
    }
  };
}