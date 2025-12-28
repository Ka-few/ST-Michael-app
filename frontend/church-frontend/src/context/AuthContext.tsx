import { createContext, useContext, useEffect, useState } from "react";
import api from "../api/api";

interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "member";
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loginUser: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("auth");
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setUser(parsed.user);
        setToken(parsed.token);
        // Set token in axios default headers
        api.defaults.headers.common["Authorization"] = `Bearer ${parsed.token}`;
        // Also store in localStorage for interceptor
        localStorage.setItem("token", parsed.token);
      } catch (error) {
        console.error("Failed to parse auth data:", error);
        localStorage.removeItem("auth");
        localStorage.removeItem("token");
      }
    }
    setLoading(false);
  }, []);

  const loginUser = (token: string, user: User) => {
    setToken(token);
    setUser(user);
    localStorage.setItem("auth", JSON.stringify({ token, user }));
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("auth");
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#C6A44A] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ user, token, loginUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}