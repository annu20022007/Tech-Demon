import { useEffect, useState } from "react";
import {
  getAdvisorRecommendations,
  chatWithAdvisor,
  getPortfolioAnalysis,
} from "../advisor.api";

export default function AdvisorPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const rec = await getAdvisorRecommendations();
        setRecommendations(rec.recommendations || []);
      } catch (e) {
        console.error("rec error", e);
      }
    };
    load();
  }, []);

  const sendMessage = async () => {
    if (!input) return;
    const userMsg = { from: "user", text: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");

    try {
      const res = await chatWithAdvisor(input);
      const botMsg = { from: "bot", text: res.response };
      setMessages((m) => [...m, botMsg]);
    } catch (e) {
      console.error(e);
    }
  };

  const analyzeDummy = async () => {
    try {
        const res = await getPortfolioAnalysis({ holdings: [] });
        setAnalysis(res.analysis);
    } catch(e) { console.error(e); }
  };

  return (
    <div className="min-h-screen p-6 space-y-6">
      <h1 className="text-2xl font-bold">AI Financial Advisor</h1>

      {/* Recommendations */}
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold mb-2">Recommendations</h2>
        <ul className="list-disc pl-6">
          {recommendations.map((rec, idx) => (
            <li key={idx} className="mb-1">
              <strong>{rec.title}:</strong> {rec.description}
            </li>
          ))}
        </ul>
      </div>

      {/* Chat */}
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold mb-2">Chat with Advisor</h2>
        <div className="border h-40 overflow-auto p-2 mb-2">
          {messages.map((m, i) => (
            <div key={i} className={m.from === "user" ? "text-right" : "text-left"}>
              <span className="inline-block px-2 py-1 rounded bg-gray-200">{m.text}</span>
            </div>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            className="flex-grow border px-2 py-1"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question..."
          />
          <button onClick={sendMessage} className="bg-blue-600 text-white px-4 py-1 rounded">
            Send
          </button>
        </div>
      </div>

      {/* Portfolio analysis demonstration */}
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold mb-2">Portfolio Analysis (demo)</h2>
        <button onClick={analyzeDummy} className="bg-green-600 text-white px-4 py-1 rounded">
          Analyze Portfolio
        </button>
        {analysis && (
          <pre className="mt-2 text-sm bg-gray-100 p-2 rounded overflow-auto">
            {JSON.stringify(analysis, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}