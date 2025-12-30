import { useState } from "react";
import { linkMemberProfile } from "../services/auth";
import { Page, Card, Input, PrimaryButton } from "../components/ui";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../api/api";

export default function LinkProfile() {
    const navigate = useNavigate();
    const { user, loginUser, token } = useAuth();

    const [claimCode, setClaimCode] = useState("");
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        try {
            await linkMemberProfile(claimCode);
            setSuccess("Profile linked successfully!");

            // Update local user context to reflect the change
            // We fetch /auth/me again to get fresh data including member_id
            try {
                const meRes = await api.get("/auth/me");
                if (token && meRes.data) {
                    loginUser(token, meRes.data);
                }
            } catch (refreshErr) {
                console.error("Failed to refresh user data", refreshErr);
            }

            setTimeout(() => {
                navigate("/");
            }, 1500);

        } catch (err: any) {
            setError(err.response?.data?.error || "Failed to link profile");
        }
    };

    if (user?.member_id) {
        return (
            <Page title="Link Profile">
                <Card className="max-w-md mx-auto text-center">
                    <p className="text-green-600 mb-4">Your account is already linked to a member profile.</p>
                    <PrimaryButton onClick={() => navigate("/")}>Go Home</PrimaryButton>
                </Card>
            </Page>
        );
    }

    return (
        <Page title="Link Member Profile">
            <Card className="max-w-md mx-auto">
                <p className="text-gray-600 mb-6 text-sm">
                    If you have a claim code from your church administrator, enter it below to link your account to your member profile.
                </p>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <Input
                        placeholder="Enter Claim Code"
                        value={claimCode}
                        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setClaimCode(e.target.value)
                        }
                        required
                    />

                    {error && <p className="text-red-500 text-sm">{error}</p>}
                    {success && <p className="text-green-500 text-sm">{success}</p>}

                    <PrimaryButton type="submit" className="w-full">
                        Link Profile
                    </PrimaryButton>
                </form>
            </Card>
        </Page>
    );
}
