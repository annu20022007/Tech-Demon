import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import LearningNavbar from "../components/LearningNavbar";
import { fetchQuizQuestions, submitQuizResult } from "../learning.api";

export default function QuizPage() {
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    const response = await fetchQuizQuestions();
    setQuestions(response.data);
    setLoading(false);
  };

  const handleNext = async () => {
    if (selectedOption === null) return;

    const correctIndex = questions[currentIndex].correctIndex;

    if (selectedOption === correctIndex) {
      setScore(score + 1);
    }

    setSelectedOption(null);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Quiz Finished
      await submitQuizResult(score + (selectedOption === correctIndex ? 1 : 0));
      navigate("/learning/progress");
    }
  };

  if (loading) {
    return (
      <>
        <LearningNavbar />
        <div className="p-10 text-center">Loading Quiz...</div>
      </>
    );
  }

  const currentQuestion = questions[currentIndex];

  return (
    <>
      <LearningNavbar />

      <div className="max-w-3xl mx-auto mt-10 bg-white p-8 rounded-2xl shadow-md">

        <h2 className="text-lg font-semibold mb-4">
          Question {currentIndex + 1} of {questions.length}
        </h2>

        <p className="text-xl font-medium mb-6">
          {currentQuestion.question}
        </p>

        <div className="space-y-4">
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => setSelectedOption(index)}
              className={`w-full text-left px-4 py-3 rounded-lg border transition ${
                selectedOption === index
                  ? "bg-green-100 border-green-500"
                  : "bg-gray-50 hover:bg-gray-100"
              }`}
            >
              {option}
            </button>
          ))}
        </div>

        <button
          onClick={handleNext}
          disabled={selectedOption === null}
          className="mt-6 w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 disabled:opacity-50"
        >
          {currentIndex + 1 === questions.length ? "Submit Quiz" : "Next"}
        </button>
      </div>
    </>
  );
}