import { useNavigate } from "react-router-dom";
import LearningNavbar from "../components/LearningNavbar";
export default function LearningHome() {
  const navigate = useNavigate();

  const cards = [
    {
      title: "Interactive Quizzes",
      description:
        "Test your financial knowledge with engaging multiple-choice quizzes.",
      route: "/learning/quiz",
      bg: "from-green-500 to-emerald-400",
    },
    {
      title: "Daily Tips",
      description:
        "Learn smart financial habits with quick daily tips and insights.",
      route: "/learning/tips",
      bg: "from-blue-500 to-indigo-400",
    },
    {
      title: "Track Progress",
      description:
        "Monitor your quiz scores and see how much you've improved.",
      route: "/learning/progress",
      bg: "from-purple-500 to-pink-400",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">

      {/* 🔹 Learning Navbar */}
      <LearningNavbar />

      {/* 🔹 Hero Section */}
      <div className="bg-gradient-to-r from-green-600 to-emerald-500 text-white py-16 text-center">
        <h1 className="text-4xl font-bold">
          Master Your Financial Knowledge
        </h1>
        <p className="mt-4 text-lg opacity-90">
          Learn through quizzes, get daily tips, and track your progress.
        </p>
      </div>

      {/* 🔹 Cards Section */}
      <div className="max-w-6xl mx-auto px-6 -mt-10">
        <div className="grid md:grid-cols-3 gap-6">

          {cards.map((card, index) => (
            <div
              key={index}
              onClick={() => navigate(card.route)}
              className={`cursor-pointer bg-gradient-to-r ${card.bg} text-white p-8 rounded-2xl shadow-lg hover:scale-105 transition-transform duration-300`}
            >
              <h2 className="text-xl font-semibold">
                {card.title}
              </h2>
              <p className="mt-4 text-sm opacity-90">
                {card.description}
              </p>
            </div>
          ))}

        </div>
      </div>

    </div>
  );
}