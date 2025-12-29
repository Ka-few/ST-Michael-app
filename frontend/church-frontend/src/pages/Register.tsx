import { useState } from "react";
import { register } from "../services/auth";
import { Page, Card, Input, PrimaryButton } from "../components/ui";
import { useNavigate } from "react-router-dom";

export default function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    claimCode: "", // <-- new field
  });

  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      // Pass claimCode to the register service
      await register(form.name, form.email, form.password, form.claimCode);
      navigate("/login");
    } catch (err: any) {
      // Display backend error
      setError(err.response?.data?.error || "Registration failed");
    }
  };

  return (
    <Page title="Create Account">
      <Card className="max-w-md mx-auto">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Full Name"
            value={form.name}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setForm({ ...form, name: e.target.value })
            }
            required
          />
          <Input
            placeholder="Email"
            value={form.email}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setForm({ ...form, email: e.target.value })
            }
            required
          />
          <Input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setForm({ ...form, password: e.target.value })
            }
            required
          />
          <Input
            placeholder="Claim Code"
            value={form.claimCode}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setForm({ ...form, claimCode: e.target.value })
            }
            required
          />

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <PrimaryButton type="submit" className="w-full">
            Register
          </PrimaryButton>
        </form>
      </Card>
    </Page>
  );
}
