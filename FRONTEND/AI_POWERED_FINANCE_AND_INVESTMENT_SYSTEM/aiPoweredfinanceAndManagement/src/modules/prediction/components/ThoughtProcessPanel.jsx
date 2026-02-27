export default function ThoughtProcessPanel({ indicators }) {
  // Support both array and object shapes for `indicators`.
  // If an object is provided (mock data), convert to an array of { name, weight }.
  const items = Array.isArray(indicators)
    ? indicators
    : Object.entries(indicators || {}).map(([key, val]) => {
        // If the value is numeric, use it as weight, otherwise default to 50
        const weight = typeof val === "number" ? val : 50;
        return { name: key, weight };
      });

  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg">
      <h2 className="text-purple-400 font-semibold mb-4">AI Thought Process</h2>

      {items.map((item, index) => (
        <div key={index} className="mb-4">
          <p className="text-sm">{item.name}</p>
          <div className="w-full bg-slate-700 rounded-full h-2 mt-1">
            <div
              className="bg-cyan-400 h-2 rounded-full"
              style={{ width: `${item.weight}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}