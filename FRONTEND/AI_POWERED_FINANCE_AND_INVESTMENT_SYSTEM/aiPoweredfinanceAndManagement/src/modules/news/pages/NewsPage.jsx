import { useEffect, useState } from "react";
import { fetchNews, fetchSentiment } from "../news.api";

export default function NewsPage() {
  const [articles, setArticles] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      try {
        const feed = await fetchNews();
        setArticles(feed.articles || feed);
      } catch (e) {
        console.error("Error loading news", e);
      }
      try {
        const s = await fetchSentiment();
        setSentiment(s);
      } catch (e) {
        console.error("Error loading sentiment", e);
      }
      setLoading(false);
    };
    load();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-pulse text-lg">Loading news...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 space-y-6">
      <h1 className="text-2xl font-bold">Financial News Feed</h1>
      {sentiment && (
        <div className="p-4 bg-white rounded shadow">
          <h2 className="font-semibold">Market Sentiment</h2>
          <p>{sentiment.overall.sentiment} ({sentiment.overall.confidence})</p>
        </div>
      )}

      <div className="grid gap-4">
        {articles.map((a, idx) => (
          <div key={idx} className="p-4 bg-white rounded shadow">
            <h3 className="font-semibold text-lg">{a.title}</h3>
            <p className="text-sm opacity-75">Source: {a.source}</p>
            <p className="mt-2">{a.summary || a.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}