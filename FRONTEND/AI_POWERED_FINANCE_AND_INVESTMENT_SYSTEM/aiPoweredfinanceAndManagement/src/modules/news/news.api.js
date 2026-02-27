import { apiFetch } from "../../services/api";

const USE_BACKEND = true; // ✅ Backend enabled

/*
 * Fetch news and market sentiment
 */
export const fetchNews = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/news/feed", {
        method: "GET",
      });
    } catch (error) {
      console.error("News fetch error:", error);
      // Fallback to mock data
      return getMockNews();
    }
  }
  return getMockNews();
};

/*
 * Fetch sentiment analysis
 */
export const fetchSentiment = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/news/sentiment", {
        method: "GET",
      });
    } catch (error) {
      console.error("Sentiment fetch error:", error);
      return getMockSentiment();
    }
  }
  return getMockSentiment();
};

/*
 * Mock news data (fallback when backend is unavailable)
 */
function getMockNews() {
  return {
    articles: [
      {
        id: 1,
        title: "Stock Market Rises on Economic Data",
        source: "Financial Times",
        sentiment: "positive",
        date: new Date().toISOString(),
        summary: "Markets respond positively to latest economic indicators showing strong growth."
      },
      {
        id: 2,
        title: "Tech Stocks Rally Amid AI Enthusiasm",
        source: "Bloomberg",
        sentiment: "positive",
        date: new Date().toISOString(),
        summary: "Technology sector gains momentum as AI investments continue to attract capital."
      },
      {
        id: 3,
        title: "Fed Holds Rates Steady",
        source: "Reuters",
        sentiment: "neutral",
        date: new Date().toISOString(),
        summary: "Federal Reserve maintains current interest rate policy as inflation shows signs of cooling."
      }
    ]
  };
}

/*
 * Mock sentiment data
 */
function getMockSentiment() {
  return {
    overall: {
      sentiment: "bullish",
      score: 0.72,
      confidence: 0.85
    },
    byCategory: {
      technology: { sentiment: "very bullish", score: 0.88 },
      finance: { sentiment: "bullish", score: 0.65 },
      healthcare: { sentiment: "neutral", score: 0.55 },
      energy: { sentiment: "bearish", score: 0.35 }
    }
  };
}
