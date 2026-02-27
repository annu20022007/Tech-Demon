// export const loginUser = async (data) => {
//   // Temporary mock login (until backend is ready)

//   if (
//     data.email === "satyaranjan9622@gmail.com" &&
//     data.password === "123456"
//   ) {
//     return {
//       user: {
//         id: 1,
//         email: data.email,
//         name: "Admin User",
//       },
//       token: "mock-jwt-token-123",
//     };
//   }

//   throw new Error("Invalid credentials");
// };
// //for backend we will modify
// import { apiFetch } from "../../services/api";

// export const loginUser = (data) =>
//   apiFetch("/auth/login", {
//     method: "POST",
//     body: JSON.stringify(data),
//   });


import { apiFetch } from "../../services/api";

const USE_BACKEND = true; // ✅ ENABLED: Now using real backend

export const loginUser = async (data) => {
  if (USE_BACKEND) {
    const response = await apiFetch("/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    });
    // Backend returns { access_token, token_type } - normalize for frontend
    return {
      token: response.access_token,
      user: {
        email: data.email,
        name: "User",
      },
    };
  }

  // 🔹 Temporary Mock Login
  if (data.email === "satyaranjan9622@gmail.com" && data.password === "123456") {
    return {
      user: {
        id: 1,
        email: data.email,
        name: "Admin User",
      },
      token: "mock-token-123",
    };
  }

  throw new Error("Invalid credentials");
};

// Register new user with real backend
export const registerUser = async (data) => {
  if (USE_BACKEND) {
    const response = await apiFetch("/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
    // Backend returns user object with id, name, email
    return {
      user: response,
      token: null, // Token comes after login
    };
  }

  // Fallback to mock
  throw new Error("Registration not available in mock mode");
};