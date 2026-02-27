import { Routes, Route } from "react-router-dom";
import MainLayout from "./layout/MainLayout";
import ProtectedRoute from "./ProtectedRoute";
import Dashboard from "../modules/dashboard/pages/Dashboard";
import LearningHome from "../modules/learning/pages/LearningHome";
import Login from "../modules/auth/pages/Login";  //real login
import Signup from "../modules/auth/pages/Signup";  //new signup
import QuizPage from "../modules/learning/pages/QuizPage";
import ProgressPage from "../modules/learning/pages/ProgressPage";
import TipsPage from "../modules/learning/pages/TipsPage";
import PredictionArena from "../modules/prediction/pages/PredictionArena";
import PortfolioDashboard from "../modules/portfolio/pages/PortfolioDashboard";





const News = () => <div>News</div>;

const Advisor = () => <div>Advisor</div>;

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* Protected Routes */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <MainLayout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
       
       <Route path="prediction" element={<PredictionArena />} />
        <Route path="news" element={<NewsPage />} />
        <Route path="/learning" element={<LearningHome />} />
        <Route path="/learning/quiz" element={<QuizPage />} />
        <Route path="/learning/tips" element={<TipsPage />} />
        <Route path="/learning/progress" element={<ProgressPage />} />
        <Route path="portfolio" element={<PortfolioDashboard />} />
        <Route path="advisor" element={<AdvisorPage />} />
      </Route>
    </Routes>
  );
}