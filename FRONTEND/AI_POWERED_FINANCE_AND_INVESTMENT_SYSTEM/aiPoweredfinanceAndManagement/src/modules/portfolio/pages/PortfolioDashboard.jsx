import { useEffect, useState } from "react";
import {
  getPortfolio,
  getPortfolioHistory,
  getAIInsight,
} from "../portfolio.api";

import AddStockForm from "../components/AddStockForm";
import PortfolioTable from "../components/PortfolioTable";
import AllocationChart from "../components/AllocationChart";
import RiskMeter from "../components/RiskMeter";
import SectorChart from "../components/SectorChart";
import PerformanceChart from "../components/PerformanceChart";
import AIInsightCard from "../components/AIInsightCard";

export default function PortfolioDashboard() {
  const [portfolio, setPortfolio] = useState([]);
  const [history, setHistory] = useState([]);
  const [insight, setInsight] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const data = await getPortfolio();
    setPortfolio(data);

    const historyData = await getPortfolioHistory();
    setHistory(historyData);

    const aiText = await getAIInsight(data);
    setInsight(aiText);
  };

  return (
    <div className="space-y-6">

      <AddStockForm onAdd={() => {}} />

      <PortfolioTable portfolio={portfolio} />

      <div className="grid md:grid-cols-2 gap-6">
        <AllocationChart portfolio={portfolio} />
        <SectorChart portfolio={portfolio} />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <PerformanceChart history={history} />
        <RiskMeter portfolio={portfolio} />
      </div>

      <AIInsightCard insight={insight} />

    </div>
  );
}