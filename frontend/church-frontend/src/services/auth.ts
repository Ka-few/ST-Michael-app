import api from "../api/api";

export interface LoginResponse {
  access_token: string;
  user: {
    id: number;
    name: string;
    email: string;
    role: "admin" | "member" | "staff";
  };
}

export const login = async (email: string, password: string) => {
  try {
    const res = await api.post<LoginResponse>("/auth/login", {
      email,
      password,
    });
    
    // Store token in localStorage after successful login
    if (res.data.access_token) {
      localStorage.setItem("token", res.data.access_token);
      // Set default Authorization header for all future requests
      api.defaults.headers.common["Authorization"] = `Bearer ${res.data.access_token}`;
    }
    
    return res.data;
  } catch (error: any) {
    console.error("Login error:", error.response?.data || error.message);
    throw error;
  }
};

export const register = async (
  name: string,
  email: string,
  password: string
) => {
  try {
    const payload = {
      name,
      email,
      password,
    };
    
    const res = await api.post("/auth/register", payload);
    return res.data;
  } catch (error: any) {
    console.error("Registration error:", error.response?.data || error.message);
    throw error;
  }
};