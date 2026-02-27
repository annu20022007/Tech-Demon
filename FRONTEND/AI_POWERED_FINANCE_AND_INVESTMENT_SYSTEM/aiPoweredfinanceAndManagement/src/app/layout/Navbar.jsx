import { useAuth } from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();          // remove user + token
    navigate("/login"); // redirect to login
  };

  return (
    <div className="flex items-center justify-between px-6 py-4 bg-white shadow-sm border-b">
      
      {/* Left Section */}
      <h1 className="text-lg font-semibold text-gray-800">
        AI Finance Platform
      </h1>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        
        {/* User Info */}
        {user && (
          <span className="text-sm text-gray-600">
            Welcome, <span className="font-medium">{user.email}</span>
          </span>
        )}

        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="bg-red-500 hover:bg-red-600 text-white text-sm px-4 py-2 rounded-lg transition"
        >
          Logout
        </button>
      </div>
    </div>
  );
}