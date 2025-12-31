import axios from "axios";

// Base URL from environment
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  console.warn("⚠️ VITE_API_BASE_URL is not set. Requests may fail.");
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ---------------- JWT Request Interceptor ----------------
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token"); // JWT stored by AuthContext
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log("🔑 JWT attached:", token.substring(0, 10) + "..."); // debug
    } else {
      console.warn("⚠️ No JWT token found in localStorage");
    }
    console.log("🌐 API URL used:", API_BASE_URL);
    return config;
  },
  (error) => Promise.reject(error)
);

// ---------------- JWT Response Interceptor ----------------
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error("🚫 Unauthorized. Clearing token and redirecting to login.");

      // Clear stored auth data
      localStorage.removeItem("access_token");
      localStorage.removeItem("auth");
      localStorage.removeItem("user");

      // Redirect to login page
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
