// src/services/auth.ts
import api from '../api/api';

interface LoginResponse {
  access_token: string;
  user: {
    id: number;
    name: string;
    email: string;
    role: "admin" | "member" | "staff";
    member_id?: number | null;
  };
}

export const login = async (email: string, password: string): Promise<LoginResponse> => {
  try {
    console.log('🔐 Attempting login for:', email);

    const res = await api.post<LoginResponse>("/auth/login", {
      email,
      password,
    });

    console.log('✅ Login successful:', res.data);

    // Don't store token here - let AuthContext handle it via loginUser()
    // This prevents duplicate/conflicting storage

    return res.data;
  } catch (error: any) {
    console.error('❌ Login failed:', error.response?.data || error.message);
    throw error;
  }
};

export const register = async (
  name: string,
  email: string,
  password: string,
  claimCode?: string
) => {
  try {
    const payload = {
      name,
      email,
      password,
      claim_code: claimCode,
    };

    const res = await api.post("/auth/register", payload);
    return res.data;
  } catch (error: any) {
    console.error("Registration error:", error.response?.data || error.message);
    throw error;
  }
};

export const linkMemberProfile = async (claimCode: string) => {
  try {
    const res = await api.post("/auth/link", { claim_code: claimCode });
    return res.data;
  } catch (error: any) {
    console.error("Link profile error:", error.response?.data || error.message);
    throw error;
  }
};