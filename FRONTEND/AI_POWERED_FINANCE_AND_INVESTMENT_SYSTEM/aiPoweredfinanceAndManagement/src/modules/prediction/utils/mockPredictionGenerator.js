export function mockPredictionGenerator() {
  const predictedPrice = 248 + Math.random() * 5;
  const actualPrice = 250 + Math.random() * 5;

  return {
    aiForecast: {
      predictedPrice: predictedPrice.toFixed(2),
      confidence: 70 + Math.floor(Math.random() * 20)
    },
    marketReality: {
      actualPrice: actualPrice.toFixed(2)
    },
    indicators: [
      { name: "Volatility Weight", weight: 45 },
      { name: "Technical RSI", weight: 30 },
      { name: "Volume Strength", weight: 25 }
    ],
    comparison: [
      { metric: "Momentum", user: 88, ai: 94 },
      { metric: "Volume", user: 82, ai: 91 },
      { metric: "Trend Fit", user: 85, ai: 93 }
    ],
    scorecard: {
      userAccuracy: 88,
      aiAccuracy: 94
    }
  };
}