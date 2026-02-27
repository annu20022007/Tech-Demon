import { useState } from "react";

export default function AddStockForm({ onAdd }) {
  const [symbol, setSymbol] = useState("");
  const [shares, setShares] = useState("");
  const [buyPrice, setBuyPrice] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    onAdd({
      symbol,
      shares: Number(shares),
      buyPrice: Number(buyPrice),
    });

    setSymbol("");
    setShares("");
    setBuyPrice("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-4 rounded-xl shadow-md grid md:grid-cols-4 gap-4"
    >
      <input
        className="border p-2 rounded"
        placeholder="Symbol"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        required
      />
      <input
        className="border p-2 rounded"
        type="number"
        placeholder="Shares"
        value={shares}
        onChange={(e) => setShares(e.target.value)}
        required
      />
      <input
        className="border p-2 rounded"
        type="number"
        placeholder="Buy Price"
        value={buyPrice}
        onChange={(e) => setBuyPrice(e.target.value)}
        required
      />
      <button className="bg-blue-600 text-white rounded p-2">
        Add
      </button>
    </form>
  );
}