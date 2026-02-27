import { useState } from "react";
import LearningNavbar from "../components/LearningNavbar";

const TIP_CATEGORIES = [
  "All",
  "Saving",
  "Budgeting",
  "Credit",
  "Investing"
];

const TIPS = [
  {
    id: 1,
    category: "Saving",
    title: "Build an Emergency Fund",
    description:
      "Aim to save 3–6 months of expenses to protect yourself from unexpected financial shocks."
  },
  {
    id: 2,
    category: "Budgeting",
    title: "Follow the 50/30/20 Rule",
    description:
      "Spend 50% on needs, 30% on wants, and 20% on savings and investments."
  },
  {
    id: 3,
    category: "Credit",
    title: "Pay Credit Cards on Time",
    description:
      "Late payments reduce your credit score and increase interest charges."
  },
  {
    id: 4,
    category: "Investing",
    title: "Diversify Your Investments",
    description:
      "Spread investments across sectors to reduce overall portfolio risk."
  },
  {
    id: 5,
    category: "Saving",
    title: "Automate Your Savings",
    description:
      "Set automatic transfers to your savings account each month."
  },
  {
    id: 6,
    category: "Investing",
    title: "Think Long-Term",
    description:
      "Long-term investing usually beats short-term speculation."
  }
];

export default function TipsPage() {
  const [activeCategory, setActiveCategory] = useState("All");

  const filteredTips =
    activeCategory === "All"
      ? TIPS
      : TIPS.filter((tip) => tip.category === activeCategory);

  return (
    <>
      <LearningNavbar />

      <div className="max-w-6xl mx-auto p-6 space-y-8">

        {/* 🔹 Header */}
        <div>
          <h1 className="text-3xl font-bold">Daily Financial Tips</h1>
          <p className="text-gray-600 mt-2">
            Quick insights to improve your financial habits.
          </p>
        </div>

        {/* 🔹 Filter Tabs */}
        <div className="flex flex-wrap gap-3">
          {TIP_CATEGORIES.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition ${
                activeCategory === category
                  ? "bg-green-600 text-white"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* 🔹 Tips Grid */}
        <div className="grid md:grid-cols-3 gap-6">
          {filteredTips.map((tip) => (
            <div
              key={tip.id}
              className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition"
            >
              <span className="text-xs font-semibold px-2 py-1 rounded bg-green-100 text-green-700">
                {tip.category}
              </span>

              <h3 className="mt-3 font-semibold text-lg">
                {tip.title}
              </h3>

              <p className="mt-2 text-sm text-gray-600">
                {tip.description}
              </p>
            </div>
          ))}
        </div>

      </div>
    </>
  );
}