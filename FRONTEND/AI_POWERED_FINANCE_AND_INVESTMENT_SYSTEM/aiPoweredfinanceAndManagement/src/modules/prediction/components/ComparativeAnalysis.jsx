export default function ComparativeAnalysis({ comparison }) {
  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
      
      <h2 className="text-yellow-400 font-semibold mb-6">
        Comparative Analysis
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left text-gray-300">
          
          <thead className="text-xs uppercase text-gray-400 border-b border-slate-700">
            <tr>
              <th className="py-3">Variable</th>
              <th className="py-3 text-center">Your Prediction</th>
              <th className="py-3 text-center">AI Prediction</th>
            </tr>
          </thead>

          <tbody>
            {comparison.map((item, index) => (
              <tr
                key={index}
                className="border-b border-slate-700 hover:bg-slate-700/40 transition"
              >
                <td className="py-4 font-medium text-white">
                  {item.metric}
                </td>

                <td className="py-4 text-center">
                  <span className="text-green-400 font-semibold">
                    {item.user}%
                  </span>
                </td>

                <td className="py-4 text-center">
                  <span className="text-cyan-400 font-semibold">
                    {item.ai}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  );
}