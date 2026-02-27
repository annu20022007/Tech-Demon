import { useEffect, useState } from "react";
import { fetchPredictionData } from "../prediction.api";

export function usePredictionEngine() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPrediction();
  }, []);

  const loadPrediction = async () => {
    setLoading(true);
    const response = await fetchPredictionData();
    setData(response);
    setLoading(false);
  };

  return { data, loading, reload: loadPrediction };
}