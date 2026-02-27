import { useEffect, useState } from "react";
import LearningNavbar from "../components/LearningNavbar";
import { fetchProgress } from "../learning.api";

export default function ProgressPage() {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    const response = await fetchProgress();
    setProgress(response.data);
    setLoading(false);
  };

  if (loading) {
    return (
      <>
        <LearningNavbar />
        <div className="p-10 text-center text-gray-500">
          Loading your progress...
        </div>
      </>
    );
  }

  const { score, totalQuestions, percentage } = progress;
  const incorrect = totalQuestions - score;

  return (
    <>
      <LearningNavbar />

      <div className="max-w-6xl mx-auto p-6 space-y-8">

        {/* 🔹 Page Header */}
        <div>
          <h1 className="text-3xl font-bold">
            Your Learning Progress
          </h1>
          <p className="text-gray-600 mt-2">
            Track your performance and monitor your improvement.
          </p>
        </div>

        {/* 🔹 Highlight Banner */}
        <div className="bg-gradient-to-r from-green-500 to-emerald-400 text-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold">
            Great Effort!
          </h2>
          <p className="mt-2">
            You scored <strong>{score} / {totalQuestions}</strong>
          </p>
        </div>

        {/* 🔹 Stats Cards */}
        <div className="grid md:grid-cols-3 lg:grid-cols-6 gap-4">

          <StatCard title="Score" value={`${score} / ${totalQuestions}`} />
          <StatCard title="Percentage" value={`${percentage}%`} />
          <StatCard title="Correct Answers" value={score} />
          <StatCard title="Incorrect Answers" value={incorrect} />
          <StatCard
            title="Status"
            value={percentage >= 70 ? "Passed" : "Needs Practice"}
          />
          <StatCard title="Attempts" value="1" />

        </div>

        {/* 🔹 Overall Performance Bar */}
        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="font-semibold mb-4">
            Overall Performance
          </h3>

          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className="bg-green-500 h-4 rounded-full transition-all duration-500"
              style={{ width: `${percentage}%` }}
            ></div>
          </div>

          <p className="mt-2 text-sm text-gray-600">
            Accuracy: {percentage}%
          </p>
        </div>

        {/* 🔹 Level Progress Section */}
        <div className="bg-white p-6 rounded-xl shadow space-y-4">
          <h3 className="font-semibold">Level Progress</h3>

          <LevelBar
            title="Budgeting Basics"
            percent={percentage}
          />
          <LevelBar
            title="Saving & Banking"
            percent={Math.max(percentage - 10, 0)}
          />
          <LevelBar
            title="Credit & Loans"
            percent={Math.max(percentage - 20, 0)}
          />
          <LevelBar
            title="Investing Basics"
            percent={Math.max(percentage - 30, 0)}
          />
        </div>

      </div>
    </>
  );
}

/* 🔹 Small Reusable Card */
function StatCard({ title, value }) {
  return (
    <div className="bg-white p-4 rounded-xl shadow text-center">
      <p className="text-sm text-gray-500">
        {title}
      </p>
      <p className="text-lg font-bold mt-2">
        {value}
      </p>
    </div>
  );
}

/* 🔹 Reusable Progress Bar */
function LevelBar({ title, percent }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span>{title}</span>
        <span>{percent}%</span>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-3">
        <div
          className="bg-green-500 h-3 rounded-full transition-all duration-500"
          style={{ width: `${percent}%` }}
        ></div>
      </div>
    </div>
  );
}