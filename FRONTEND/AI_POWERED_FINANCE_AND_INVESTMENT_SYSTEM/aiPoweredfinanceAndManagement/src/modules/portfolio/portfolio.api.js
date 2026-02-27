import { apiFetch } from "../../services/api";

const USE_BACKEND = true; // ✅ Backend enabled

// sector mapping (for mock data only)
const sectorMap = {
  AAPL: "Technology",
  MSFT: "Technology",
  TSLA: "Automotive",
  GOOGL: "Technology",
  XOM: "Energy",
};

// Mock portfolio data
const mockPortfolioData = [
  { id: 1, symbol: "AAPL", shares: 45, buyPrice: 300 },
  { id: 2, symbol: "MSFT", shares: 32, buyPrice: 390 },
  { id: 3, symbol: "TSLA", shares: 22, buyPrice: 210 },
];

function simulatePrice(buyPrice) {
  const randomGrowth = 1 + Math.random() * 0.2;
  return buyPrice * randomGrowth;
}

/*
 * Get user portfolio holdings
 */
export const getPortfolio = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/portfolio", {
        method: "GET",
      });
    } catch (error) {
      console.error("Portfolio fetch error:", error);
      return getMockPortfolio();
    }
  }
  return getMockPortfolio();
};

/*
 * Get portfolio history/performance over time
 */
export const getPortfolioHistory = async () => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/portfolio/history", {
        method: "GET",
      });
    } catch (error) {
      console.error("Portfolio history fetch error:", error);
      return getMockPortfolioHistory();
    }
  }
  return getMockPortfolioHistory();
};

/*
 * Get AI insight about portfolio
 */
export const getAIInsight = async (portfolio) => {
  if (USE_BACKEND) {
    try {
      return await apiFetch("/portfolio/insight", {
        method: "POST",
        body: JSON.stringify({ portfolio }),
      });
    } catch (error) {
      console.error("Portfolio insight error:", error);
      return getMockInsight(portfolio);
    }
  }
  return getMockInsight(portfolio);
};

/*
 * Mock portfolio data
 */
function getMockPortfolio() {
  return mockPortfolioData.map((stock) => ({
    ...stock,
    currentPrice: simulatePrice(stock.buyPrice),
    sector: sectorMap[stock.symbol] || "Other",
  }));
}

/*
 * Mock portfolio history
 */
function getMockPortfolioHistory() {
  return Array.from({ length: 6 }).map((_, i) => ({
    month: `M${i + 1}`,
    value: 10000 + Math.random() * 5000,
  }));
}

/*
 * Mock portfolio insight
 */
function getMockInsight(portfolio) {
  if (!portfolio || portfolio.length === 0) {
    return "Add stocks to your portfolio to get AI insights.";
  }

  const techWeight =
    portfolio.filter((s) => s.sector === "Technology").length /
    portfolio.length;

  if (techWeight > 0.6)
    return "Your portfolio is heavily tech concentrated. Consider diversification.";

  return "Portfolio is reasonably diversified with moderate risk exposure.";
}