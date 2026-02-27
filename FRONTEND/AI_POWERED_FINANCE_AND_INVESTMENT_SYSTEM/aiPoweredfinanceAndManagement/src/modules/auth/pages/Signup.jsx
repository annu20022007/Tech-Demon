import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser, loginUser } from "../auth.api";
import { useAuth } from "../../../context/AuthContext";

export default function Signup() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!formData.name || !formData.email || !formData.password) {
      setError("All fields are required");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    setLoading(true);

    try {
      // Register user
      const registerResponse = await registerUser({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      });

      console.log("Register Response:", registerResponse);

      // Auto-login after successful registration
      const loginResponse = await loginUser({
        email: formData.email,
        password: formData.password,
      });

      console.log("Login Response:", loginResponse);

      login(loginResponse.user, loginResponse.token);
      navigate("/"); // go to dashboard
    } catch (err) {
      console.error("Signup Error:", err);
      setError(err.message || "Registration failed. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white shadow-md rounded-xl p-8 w-96"
      >
        <h2 className="text-2xl font-bold text-center mb-2">
          Create Account
        </h2>
        <p className="text-center text-sm text-gray-600 mb-6">
          Join our community for financial learning
        </p>

        {error && (
          <p className="text-red-500 text-sm mb-4 bg-red-50 p-2 rounded">
            {error}
          </p>
        )}

        <div className="mb-4">
          <label className="block mb-1 text-sm font-medium">
            Full Name
          </label>
          <input
            type="text"
            name="name"
            className="w-full border rounded-lg p-3"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1 text-sm font-medium">
            Email
          </label>
          <input
            type="email"
            name="email"
            className="w-full border rounded-lg p-3"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-4">
          <label className="block mb-1 text-sm font-medium">
            Password
          </label>
          <input
            type="password"
            name="password"
            className="w-full border rounded-lg p-3"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-6">
          <label className="block mb-1 text-sm font-medium">
            Confirm Password
          </label>
          <input
            type="password"
            name="confirmPassword"
            className="w-full border rounded-lg p-3"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 transition font-medium"
        >
          {loading ? "Creating Account..." : "Sign Up"}
        </button>

        <p className="text-center text-sm mt-4">
          Already have an account?{" "}
          <button
            type="button"
            onClick={() => navigate("/login")}
            className="text-blue-600 hover:underline font-medium"
          >
            Login here
          </button>
        </p>
      </form>
    </div>
  );
}
