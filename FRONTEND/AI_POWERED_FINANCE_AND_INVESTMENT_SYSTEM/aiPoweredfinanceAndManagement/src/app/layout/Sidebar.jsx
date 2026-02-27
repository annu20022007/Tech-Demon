import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  BookOpen,
  TrendingUp,
  Newspaper,
  Briefcase,
  Bot,
} from "lucide-react";

export default function Sidebar() {
  const linkStyle =
    "flex items-center gap-3 px-4 py-3 rounded-lg transition text-sm font-medium";

  const activeStyle = "bg-blue-100 text-blue-700";
  const inactiveStyle = "text-gray-600 hover:bg-gray-100";

  return (
    <aside className="w-64 bg-white shadow-md p-5 flex flex-col">
      
      {/* Logo / Title */}
      <div className="mb-8">
        <h2 className="text-xl font-bold text-blue-700">
          AI Finance
        </h2>
      </div>

      {/* Navigation Links */}
      <nav className="flex flex-col gap-2">

        <NavLink
          to="/"
          className={({ isActive }) =>
            `${linkStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          <LayoutDashboard size={18} />
          Dashboard
        </NavLink>

        <NavLink
          to="/learning"
          className={({ isActive }) =>
            `${linkStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          <BookOpen size={18} />
          Learning
        </NavLink>

        <NavLink
          to="/prediction"
          className={({ isActive }) =>
            `${linkStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          <TrendingUp size={18} />
          Prediction
        </NavLink>

        <NavLink
          to="/news"
          className={({ isActive }) =>
            `${linkStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          <Newspaper size={18} />
          News
        </NavLink>

        <NavLink
          to="/portfolio"
          className={({ isActive }) =>
            `${linkStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          <Briefcase size={18} />
          Portfolio
        </NavLink>

        <NavLink
          to="/advisor"
          className={({ isActive }) =>
            `${linkStyle} ${isActive ? activeStyle : inactiveStyle}`
          }
        >
          <Bot size={18} />
          AI Advisor
        </NavLink>

      </nav>
    </aside>
  );
}