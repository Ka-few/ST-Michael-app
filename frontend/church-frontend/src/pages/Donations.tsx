import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import api from "../api/api";

interface Donation {
  id: number;
  user_id?: number;
  amount: number;
  type: string;
  date: string | null;
  created_at?: string;
}

export default function Donations() {
  const { user } = useAuth();
  const [donations, setDonations] = useState<Donation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);
  
  const [form, setForm] = useState({
    user_id: "",
    amount: "",
    type: "tithe",
    date: new Date().toISOString().split('T')[0]
  });

  const fetchDonations = async () => {
    setLoading(true);
    setError("");
    
    try {
      const endpoint = user?.role === "admin" 
        ? "/donations/" 
        : "/donations/my-donations";
      
      const response = await api.get(endpoint);
      setDonations(response.data);
    } catch (error: any) {
      console.error("Failed to fetch donations:", error);
      setError(error.response?.data?.error || "Failed to load donations");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDonations();
  }, [user]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    
    try {
      const payload = user?.role === "admin"
        ? { ...form, user_id: Number(form.user_id), amount: Number(form.amount) }
        : { amount: Number(form.amount), type: form.type, date: form.date };
      
      const endpoint = user?.role === "admin" ? "/donations/admin/add" : "/donations/";
      
      await api.post(endpoint, payload);
      
      setForm({
        user_id: "",
        amount: "",
        type: "tithe",
        date: new Date().toISOString().split('T')[0]
      });
      setShowForm(false);
      fetchDonations();
    } catch (error: any) {
      setError(error.response?.data?.error || "Failed to create donation");
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this donation?")) {
      return;
    }
    
    try {
      const endpoint = user?.role === "admin" 
        ? `/donations/admin/${id}` 
        : `/donations/${id}`;
      
      await api.delete(endpoint);
      fetchDonations();
    } catch (error: any) {
      setError(error.response?.data?.error || "Failed to delete donation");
    }
  };

  const totalDonations = donations.reduce((sum, d) => sum + d.amount, 0);

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">
          {user?.role === "admin" ? "All Donations" : "My Donations"}
        </h1>
        
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-6 py-2 bg-[#C6A44A] text-white rounded-lg hover:bg-[#B5934A]"
        >
          {showForm ? "Cancel" : user?.role === "admin" ? "Add Donation" : "Make a Donation"}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Donation Form */}
      {showForm && (
        <div className="bg-white p-6 rounded-xl shadow border border-[#E6D8A3] mb-6">
          <h2 className="text-xl font-semibold text-[#C9A227] mb-4">
            {user?.role === "admin" ? "Add Donation Record" : "Make a Donation"}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {user?.role === "admin" && (
              <div>
                <label className="block text-sm font-medium mb-1">User ID</label>
                <input
                  name="user_id"
                  type="number"
                  value={form.user_id}
                  onChange={handleChange}
                  className="w-full border rounded-lg px-3 py-2"
                  placeholder="User ID"
                  required
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium mb-1">Amount (KES)</label>
              <input
                name="amount"
                type="number"
                step="0.01"
                min="1"
                value={form.amount}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                placeholder="1000"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Type</label>
              <select
                name="type"
                value={form.type}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                required
              >
                <option value="tithe">Tithe</option>
                <option value="offering">Offering</option>
                <option value="thanksgiving">Thanksgiving</option>
                <option value="building_fund">Building Fund</option>
                <option value="special">Special Offering</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Date</label>
              <input
                name="date"
                type="date"
                value={form.date}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full bg-[#C9A227] text-white rounded-lg hover:bg-[#B8961E] px-4 py-3"
            >
              Submit Donation
            </button>
          </form>
        </div>
      )}

      {/* Summary Card */}
      <div className="bg-gradient-to-r from-[#C6A44A] to-[#B8961E] text-white p-6 rounded-xl shadow mb-6">
        <h2 className="text-lg font-semibold mb-2">Total Donations</h2>
        <p className="text-4xl font-bold">KES {totalDonations.toLocaleString()}</p>
        <p className="text-sm mt-2 opacity-90">{donations.length} donation(s)</p>
      </div>

      {/* Donations List */}
      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#C6A44A] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading donations...</p>
        </div>
      ) : (
        <div className="space-y-4">
          {donations.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <p className="text-gray-500">No donations recorded yet.</p>
            </div>
          ) : (
            donations.map((donation) => (
              <div
                key={donation.id}
                className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    {user?.role === "admin" && (
                      <p className="text-sm text-gray-500 mb-1">User #{donation.user_id}</p>
                    )}
                    <p className="font-bold text-2xl text-[#C9A227]">
                      KES {donation.amount.toLocaleString()}
                    </p>
                    <p className="text-gray-600 capitalize mt-1">
                      {donation.type.replace('_', ' ')}
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      {donation.date ? new Date(donation.date).toLocaleDateString() : 'No date'}
                    </p>
                  </div>
                  
                  <button
                    onClick={() => handleDelete(donation.id)}
                    className="text-red-600 text-sm hover:underline"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}