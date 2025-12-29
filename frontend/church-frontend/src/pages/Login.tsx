import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login } from "../services/auth";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { loginUser } = useAuth();
  
  const [form, setForm] = useState({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    
    try {
      const data = await login(form.email, form.password);
      console.log('Full login response:', data);
      
      // Use access_token from response
      loginUser(data.access_token, data.user);
      navigate("/");
    } catch (err: any) {
      console.error("Login error:", err);
      setError(err.response?.data?.error || "Login failed");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#FAF6E8]">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input
              type="email"
              required
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C6A44A]"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input
              type="password"
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-[#C6A44A]"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-[#C6A44A] text-white py-2 rounded-lg hover:bg-[#B5934A]"
          >
            Login
          </button>
        </form>

        <p className="text-center mt-4 text-sm">
          Don't have an account?{" "}
          <Link to="/register" className="text-[#C6A44A] hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  );
}