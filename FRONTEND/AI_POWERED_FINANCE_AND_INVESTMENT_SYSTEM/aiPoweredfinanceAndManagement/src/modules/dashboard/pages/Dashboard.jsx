import { useEffect, useState } from "react";
import {
  getDashboardStats,
  getPerformanceData,
  getSentimentData,
  getDashboardInsight,
} from "../dashboard.api";

import StatCard from "../components/StatCard";
import PerformanceChart from "../components/PerformanceChart";
import SentimentChart from "../components/SentimentChart";
import InsightCard from "../components/InsightCard";

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [performance, setPerformance] = useState([]);
  const [sentiment, setSentiment] = useState([]);
  const [insight, setInsight] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();

    const interval = setInterval(() => {
      loadData();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    setLoading(true);

    const statsData = await getDashboardStats();
    const perfData = await getPerformanceData();
    const sentimentData = await getSentimentData();
    const insightData = await getDashboardInsight();

    setStats(statsData);
    setPerformance(perfData);
    setSentiment(sentimentData);
    setInsight(insightData);

    setLoading(false);
  };

  if (loading) {
    return (
      <div className="animate-pulse space-y-6">
        <div className="h-24 bg-gray-200 rounded-xl"></div>
        <div className="h-64 bg-gray-200 rounded-xl"></div>
        <div className="h-20 bg-gray-200 rounded-xl"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {/* Top Cards */}
      <div className="grid md:grid-cols-4 gap-4">
        <StatCard title="Market Sentiment" value={stats.marketSentiment} color="red" />
        <StatCard title="AI Prediction" value={stats.aiPrediction} color="orange" />
        <StatCard title="Portfolio Risk" value={stats.portfolioRisk} color="yellow" />
        <StatCard title="AI Confidence" value={`${stats.aiConfidence}%`} color="blue" />
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        <PerformanceChart data={performance} />
        <SentimentChart data={sentiment} />
      </div>

      {/* Insight */}
      <InsightCard text={insight} />

    </div>
  );
}