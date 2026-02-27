import { NavLink } from "react-router-dom";

export default function LearningNavbar() {
  const navItems = [
    { name: "Home", path: "/learning" },
    { name: "Quizzes", path: "/learning/quiz" },
    { name: "Tips", path: "/learning/tips" },
    { name: "Progress", path: "/learning/progress" },
  ];

  return (
    <div className="sticky top-0 z-50 bg-white shadow-sm border-b">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo / Title */}
          <h2 className="text-xl font-bold text-green-600">
            Learning Center
          </h2>

          {/* Navigation */}
          <div className="flex gap-6">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors ${
                    isActive
                      ? "text-green-600 border-b-2 border-green-600 pb-1"
                      : "text-gray-600 hover:text-green-600"
                  }`
                }
              >
                {item.name}
              </NavLink>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}