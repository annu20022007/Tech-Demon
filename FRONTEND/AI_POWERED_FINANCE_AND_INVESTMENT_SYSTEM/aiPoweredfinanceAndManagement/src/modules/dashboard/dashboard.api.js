import { apiFetch } from "../../services/api";

const USE_BACKEND = true; // ✅ Backend enabled

// ---- MOCK DATA (Fallback) ----
const mockDashboard = {
  marketSentiment: "Bullish",
  aiPrediction: "Uptrend",
  portfolioRisk: "Moderate Risk",
  aiConfidence: 75,
};

const mockPerformance = [
  { date: "Mar 1", value: 18500 },
  { date: "Mar 8", value: 19000 },
  { date: "Mar 15", value: 20000 },
  { date: "Mar 22", value: 21000 },
  { date: "Mar 29", value: 22000 },
];

const mockSentiment = [
  { week: "Week 1", positive: 18, negative: 10 },
  { week: "Week 2", positive: 22, negative: 5 },
  { week: "Week 3", positive: 25, negative: 8 },
  { week: "Week 4", positive: 28, negative: 5 },
];

const mockInsight =
  "Your portfolio is well-diversified with strong growth in tech and healthcare sectors. Market sentiment is bullish for Q2. Consider taking profits on top performers.";

// ---- API FUNCTIONS ----
export const getDashboardStats = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/dashboard/stats");
    } catch (error) {
      console.error("Dashboard stats fetch error:", error);
      return mockDashboard;
    }
  }
  return mockDashboard;
};

export const getPerformanceData = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/dashboard/performance");
    } catch (error) {
      console.error("Performance data fetch error:", error);
      return mockPerformance;
    }
  }
  return mockPerformance;
};

export const getSentimentData = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/dashboard/sentiment");
    } catch (error) {
      console.error("Sentiment data fetch error:", error);
      return mockSentiment;
    }
  }
  return mockSentiment;
};

export const getDashboardInsight = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/dashboard/insight");
    } catch (error) {
      console.error("Dashboard insight fetch error:", error);
      return mockInsight;
    }
  }
  return mockInsight;
};