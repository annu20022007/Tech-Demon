import { useState } from "react";
import { motion } from "framer-motion";

export default function PredictionControls({ aiDirection, confidence }) {
  const [userChoice, setUserChoice] = useState(null);
  const [showResult, setShowResult] = useState(false);

  const handlePrediction = (choice) => {
    setUserChoice(choice);
    setTimeout(() => {
      setShowResult(true);
    }, 600);
  };

  const isMatch = userChoice === aiDirection;

  const generateExplanation = () => {
    if (!userChoice) return "";

    if (isMatch) {
      return "Your prediction aligns with AI analysis. Strong indicator agreement and supportive market signals reinforce this direction.";
    } else {
      return "Your prediction differs from AI analysis. Market volatility and technical indicators suggest a different movement outlook.";
    }
  };

  return (
    <div className="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700 space-y-6">

      <h2 className="text-cyan-400 font-semibold text-lg">
        Make Your Prediction
      </h2>

      {/* Buttons */}
      <div className="flex gap-4">
        <button
          onClick={() => handlePrediction("UP")}
          className="flex-1 bg-green-600 hover:bg-green-700 transition py-3 rounded-lg font-semibold"
        >
          Predict UP
        </button>

        <button
          onClick={() => handlePrediction("DOWN")}
          className="flex-1 bg-red-600 hover:bg-red-700 transition py-3 rounded-lg font-semibold"
        >
          Predict DOWN
        </button>
      </div>

      {/* Animated Result */}
      {showResult && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-slate-700 p-5 rounded-lg space-y-3"
        >
          <div className="flex justify-between text-sm">
            <span>Your Prediction:</span>
            <span className="font-semibold text-white">
              {userChoice}
            </span>
          </div>

          <div className="flex justify-between text-sm">
            <span>AI Prediction:</span>
            <span className="font-semibold text-cyan-300">
              {aiDirection}
            </span>
          </div>

          <div className="flex justify-between text-sm">
            <span>AI Confidence:</span>
            <span className="text-green-400 font-semibold">
              {confidence}%
            </span>
          </div>

          <div className="mt-4 text-sm text-gray-300">
            <strong>AI Explanation:</strong>
            <p className="mt-1">
              {generateExplanation()}
            </p>
          </div>

          <div className="mt-3 text-center">
            {isMatch ? (
              <span className="text-green-400 font-bold">
                ✔ You matched AI prediction!
              </span>
            ) : (
              <span className="text-red-400 font-bold">
                ✖ Prediction differs from AI
              </span>
            )}
          </div>
        </motion.div>
      )}
    </div>
  );
}