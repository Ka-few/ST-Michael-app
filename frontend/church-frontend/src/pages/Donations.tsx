import { useEffect, useState } from 'react';
import api from '../api/api';
import type { Donation } from '../type/models';



export default function Donations() {
  const [donations, setDonations] = useState<Donation[]>([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({ member_id: '', amount: '', type: 'tithe', date: '' });
  const [editId, setEditId] = useState<number | null>(null);

  const fetchDonations = () => {
    setLoading(true);
    api.get('/donations/')
      .then(res => setDonations(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => fetchDonations(), []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { ...form, member_id: Number(form.member_id), amount: Number(form.amount) };
    if (editId) {
      api.put(`/donations/${editId}`, payload).then(() => {
        fetchDonations();
        setForm({ member_id: '', amount: '', type: 'tithe', date: '' });
        setEditId(null);
      });
    } else {
      api.post('/donations/', payload).then(() => {
        fetchDonations();
        setForm({ member_id: '', amount: '', type: 'tithe', date: '' });
      });
    }
  };

  const handleEdit = (d: Donation) => {
    setForm({ member_id: String(d.member_id), amount: String(d.amount), type: d.type, date: d.date || '' });
    setEditId(d.id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Delete this donation?')) api.delete(`/donations/${id}`).then(fetchDonations);
  };

  return (
  <div className="bg-white p-6 rounded-xl shadow border border-[#E6D8A3]">
    <h2 className="text-xl font-semibold text-[#C9A227] mb-4">
      {editId ? "Edit Donation" : "Record Donation"}
    </h2>

    <form
      onSubmit={handleSubmit}
      className="grid md:grid-cols-5 gap-4"
    >
      <input
        name="member_id"
        value={form.member_id}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
        placeholder="Member ID"
        required
      />

      <input
        name="amount"
        type="number"
        value={form.amount}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
        placeholder="Amount"
        required
      />

      <select
        name="type"
        value={form.type}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
      >
        <option value="tithe">Tithe</option>
        <option value="offering">Offering</option>
      </select>

      <input
        name="date"
        type="date"
        value={form.date}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
      />

      <button
        type="submit"
        className="bg-[#C9A227] text-white rounded-lg hover:bg-[#B8961E] px-4 py-2"
      >
        {editId ? "Update" : "Save"}
      </button>
    </form>

    {loading ? (
      <p className="mt-6">Loading donations...</p>
    ) : (
      <div className="mt-6 grid md:grid-cols-3 gap-4">
        {donations.map(d => (
          <div
            key={d.id}
            className="border rounded-lg p-4 shadow-sm"
          >
            <p className="font-semibold">
              Member #{d.member_id}
            </p>
            <p>KES {d.amount}</p>
            <p className="text-sm text-gray-600 capitalize">
              {d.type}
            </p>
            <p className="text-sm text-gray-500">
              {d.date}
            </p>

            <div className="flex gap-3 mt-2">
              <button
                onClick={() => handleEdit(d)}
                className="text-blue-600 text-sm"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(d.id)}
                className="text-red-600 text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

}
