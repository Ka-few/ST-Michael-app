import { useState } from "react";
import { login } from "../services/auth";
import { useAuth } from "../context/AuthContext";
import { Page, Card, Input, PrimaryButton } from "../components/ui";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login(email, password);
      loginUser(res.access_token, res.user as any);

      // 🔀 Role-based redirect
      if (res.user.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/announcements");
      }
    } catch {
      setError("Invalid email or password");
    }
  };

  return (
    <Page title="Login">
      <Card className="max-w-md mx-auto">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Email"
            value={email}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
            required
          />

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <PrimaryButton type="submit" className="w-full">
            Sign In
          </PrimaryButton>
        </form>
      </Card>
    </Page>
  );
}
