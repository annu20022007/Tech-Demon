export default function PortfolioTable({ portfolio }) {
  return (
    <div className="bg-white p-4 rounded-xl shadow-md overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b">
            <th>Symbol</th>
            <th>Shares</th>
            <th>Buy</th>
            <th>Current</th>
            <th>Value</th>
            <th>P/L</th>
          </tr>
        </thead>
        <tbody>
          {portfolio.map((stock) => {
            const value = stock.shares * stock.currentPrice;
            const invested = stock.shares * stock.buyPrice;
            const profit = value - invested;

            return (
              <tr key={stock.id} className="border-b">
                <td>{stock.symbol}</td>
                <td>{stock.shares}</td>
                <td>${stock.buyPrice}</td>
                <td>${stock.currentPrice.toFixed(2)}</td>
                <td>${value.toFixed(2)}</td>
                <td
                  className={
                    profit >= 0
                      ? "text-green-600"
                      : "text-red-600"
                  }
                >
                  ${profit.toFixed(2)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}