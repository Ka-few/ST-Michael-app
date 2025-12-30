// src/context/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';

interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "member" | "staff";
  member_id?: number | null;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  loginUser: (token: string, user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Initialize auth from localStorage on mount
  useEffect(() => {
    console.log('🔍 Checking for existing auth...');

    const stored = localStorage.getItem("auth");
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setUser(parsed.user);
        setToken(parsed.token);

        // CRITICAL: Store as 'access_token' for api.ts interceptor
        localStorage.setItem("access_token", parsed.token);

        console.log('✅ Auth restored:', parsed.user.email);
        console.log('✅ Token stored as access_token');
      } catch (error) {
        console.error('❌ Failed to parse auth data:', error);
        localStorage.removeItem("auth");
        localStorage.removeItem("access_token");
      }
    } else {
      console.log('⚠️ No stored auth found');
    }

    setLoading(false);
  }, []);

  const loginUser = (newToken: string, newUser: User) => {
    console.log('🔐 Logging in user:', newUser.email);

    setToken(newToken);
    setUser(newUser);

    // Store in auth object (your existing pattern)
    localStorage.setItem("auth", JSON.stringify({ token: newToken, user: newUser }));

    // CRITICAL: Also store as 'access_token' for api.ts interceptor
    localStorage.setItem("access_token", newToken);

    // Verify storage
    const verify = localStorage.getItem('access_token');
    console.log('✅ Token stored:', !!verify);
    console.log('✅ Token preview:', verify?.substring(0, 20) + '...');
  };

  const logout = () => {
    console.log('👋 Logging out user');

    setToken(null);
    setUser(null);

    localStorage.removeItem("auth");
    localStorage.removeItem("access_token");
    localStorage.removeItem("token"); // Remove old key if it exists
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
    <AuthContext.Provider
      value={{
        user,
        token,
        loginUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};