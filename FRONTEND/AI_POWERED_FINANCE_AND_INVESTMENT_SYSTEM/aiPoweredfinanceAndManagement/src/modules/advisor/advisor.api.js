import { apiFetch } from "../../services/api";

const USE_BACKEND = true; // ✅ Backend enabled

/*
 * Get AI financial advisor recommendations
 */
export const getAdvisorRecommendations = async (userProfile = {}) => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/advisor/recommendations", {
        method: "POST",
        body: JSON.stringify(userProfile),
      });
    } catch (error) {
      console.error("Advisor recommendations fetch error:", error);
      return getMockRecommendations();
    }
  }
  return getMockRecommendations();
};

/*
 * Chat with AI advisor
 */
export const chatWithAdvisor = async (message) => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/advisor/chat", {
        method: "POST",
        body: JSON.stringify({ message }),
      });
    } catch (error) {
      console.error("Advisor chat error:", error);
      return getMockChatResponse(message);
    }
  }
  return getMockChatResponse(message);
};

/*
 * Get portfolio analysis from advisor
 */
export const getPortfolioAnalysis = async (portfolio) => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/advisor/portfolio-analysis", {
        method: "POST",
        body: JSON.stringify(portfolio),
      });
    } catch (error) {
      console.error("Portfolio analysis error:", error);
      return getMockPortfolioAnalysis();
    }
  }
  return getMockPortfolioAnalysis();
};

/*
 * Mock advisor recommendations (fallback when backend is unavailable)
 */
function getMockRecommendations() {
  return {
    recommendations: [
      {
        id: 1,
        title: "Diversify Your Portfolio",
        description: "Consider adding more tech stocks to balance your current holdings.",
        priority: "high",
        confidence: 0.85,
        actionItems: [
          "Increase exposure to AI/ML companies",
          "Reduce concentration in finance sector"
        ]
      },
      {
        id: 2,
        title: "Rebalance Monthly",
        description: "Monthly rebalancing helps maintain your target asset allocation.",
        priority: "medium",
        confidence: 0.78,
        actionItems: [
          "Set reminder for first of each month",
          "Review sector weightings"
        ]
      },
      {
        id: 3,
        title: "Start an Emergency Fund",
        description: "Build 6 months of expenses in liquid savings.",
        priority: "high",
        confidence: 0.92,
        actionItems: [
          "Open high-yield savings account",
          "Schedule automatic monthly transfers"
        ]
      }
    ]
  };
}

/*
 * Mock chat response
 */
function getMockChatResponse(message) {
  const responses = {
    portfolio: "Based on your portfolio, I recommend increasing diversification...",
    risk: "Your risk tolerance appears moderate. Consider a 60/40 stock/bond allocation...",
    stocks: "Tech stocks are showing strong growth momentum. However, consider your risk profile...",
    default: "I'm here to help! Ask me about portfolio strategy, market trends, or risk management."
  };

  const key = Object.keys(responses).find(k => message.toLowerCase().includes(k)) || "default";
  
  return {
    message: responses[key],
    timestamp: new Date().toISOString(),
    confidence: 0.85
  };
}

/*
 * Mock portfolio analysis
 */
function getMockPortfolioAnalysis() {
  return {
    overview: {
      totalValue: 50000,
      dayGain: 250,
      dayGainPercent: 0.5,
      YTDReturn: 12.5
    },
    riskAssessment: {
      level: "moderate",
      score: 6.5,
      recommendation: "Well-balanced portfolio for long-term growth"
    },
    allocation: {
      stocks: 65,
      bonds: 25,
      cash: 10
    },
    topHoldings: [
      { symbol: "AAPL", percentage: 15, gain: 5.2 },
      { symbol: "MSFT", percentage: 12, gain: 8.1 },
      { symbol: "TSLA", percentage: 10, gain: -2.3 }
    ],
    suggestions: [
      "Consider tax-loss harvesting opportunities",
      "Rebalance sector allocations quarterly"
    ]
  };
}
