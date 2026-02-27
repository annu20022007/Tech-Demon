// Import mock questions
import { QUIZ_QUESTIONS } from "./learning.constants";
import { apiFetch } from "../../services/api";

/*
  Toggle this to true when backend is ready
*/
const USE_BACKEND = true;

/*
  Simulate network delay
*/
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/* =========================================================
   FETCH QUIZ QUESTIONS
========================================================= */

export async function fetchQuizQuestions() {
  if (USE_BACKEND) {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/learning/quiz`
    );
    return await response.json();
  }

  // Mock mode
  await delay(500);

  return {
    success: true,
    data: QUIZ_QUESTIONS,
  };
}

/* =========================================================
   SUBMIT QUIZ RESULT
========================================================= */

export async function submitQuizResult(score, totalQuestions = 10) {
  if (USE_BACKEND) {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/learning/submit`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ score, totalQuestions }),
      }
    );

    return await response.json();
  }

  // Mock mode
  await delay(300);

  const result = {
    score,
    totalQuestions,
    percentage: Math.round((score / totalQuestions) * 100),
    date: new Date().toISOString(),
  };

  localStorage.setItem("quizResult", JSON.stringify(result));

  return {
    success: true,
    message: "Result saved successfully",
  };
}

/* =========================================================
   FETCH PROGRESS DATA
========================================================= */

export async function fetchProgress() {
  if (USE_BACKEND) {
    const response = await fetch(
      `${import.meta.env.VITE_API_URL}/learning/progress`
    );
    return await response.json();
  }

  // Mock mode
  await delay(300);

  const stored = localStorage.getItem("quizResult");

  if (!stored) {
    return {
      success: true,
      data: {
        score: 0,
        totalQuestions: 10,
        percentage: 0,
        date: null,
      },
    };
  }

  return {
    success: true,
    data: JSON.parse(stored),
  };
}