import api from "../api/api";

export interface LoginResponse {
  access_token: string;
  user: {
    id: number;
    name: string;
    email: string;
    role: "admin" | "member";
  };
}

export const login = async (email: string, password: string) => {
  const res = await api.post<LoginResponse>("/auth/login", {
    email,
    password,
  });
  return res.data;
};

export const register = async (
  name: string,
  email: string,
  password: string
) => {
  const res = await api.post("/auth/register", {
    name,
    email,
    password,
  });
  return res.data;
};
