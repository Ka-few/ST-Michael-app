import { useEffect, useState } from 'react';
import api from '../api/api';
import type { Sacrament } from '../type/models';



export default function Sacraments() {
  const [sacraments, setSacraments] = useState<Sacrament[]>([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({ member_id: '', type: '', date: '' });
  const [editId, setEditId] = useState<number | null>(null);

  const fetchSacraments = () => {
    setLoading(true);
    api.get('/sacraments/')
      .then(res => setSacraments(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => fetchSacraments(), []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { ...form, member_id: Number(form.member_id) };
    if (editId) {
      api.put(`/sacraments/${editId}`, payload).then(() => {
        fetchSacraments();
        setForm({ member_id: '', type: '', date: '' });
        setEditId(null);
      });
    } else {
      api.post('/sacraments/', payload).then(() => {
        fetchSacraments();
        setForm({ member_id: '', type: '', date: '' });
      });
    }
  };

  const handleEdit = (s: Sacrament) => {
    setForm({ member_id: String(s.member_id), type: s.type, date: s.date || '' });
    setEditId(s.id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Delete this sacrament?')) api.delete(`/sacraments/${id}`).then(fetchSacraments);
  };

  return (
  <div className="bg-white p-6 rounded-xl shadow border border-[#E6D8A3]">
    <h2 className="text-xl font-semibold text-[#C9A227] mb-4">
      {editId ? "Edit Sacrament" : "Add Sacrament"}
    </h2>

    <form
      onSubmit={handleSubmit}
      className="grid md:grid-cols-4 gap-4"
    >
      <input
        name="member_id"
        value={form.member_id}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
        placeholder="Member ID"
        required
      />

      <select
        name="type"
        value={form.type}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
        required
      >
        <option value="">Select Sacrament</option>
        <option value="baptism">Baptism</option>
        <option value="confirmation">Confirmation</option>
        <option value="communion">Holy Communion</option>
        <option value="marriage">Marriage</option>
        <option value="holy_orders">Holy Orders</option>
        <option value="anointing">Anointing of the Sick</option>
      </select>

      <input
        name="date"
        type="date"
        value={form.date}
        onChange={handleChange}
        className="border rounded-lg px-3 py-2"
        required
      />

      <button
        type="submit"
        className="bg-[#C9A227] text-white rounded-lg hover:bg-[#B8961E] px-4 py-2"
      >
        {editId ? "Update" : "Add"}
      </button>
    </form>

    {loading ? (
      <p className="mt-6">Loading sacraments...</p>
    ) : (
      <div className="mt-6 grid md:grid-cols-3 gap-4">
        {sacraments.map(s => (
          <div
            key={s.id}
            className="border rounded-lg p-4 shadow-sm"
          >
            <p className="font-semibold">
              Member #{s.member_id}
            </p>
            <p className="capitalize">{s.type.replace("_", " ")}</p>
            <p className="text-sm text-gray-500">{s.date}</p>

            <div className="flex gap-3 mt-2">
              <button
                onClick={() => handleEdit(s)}
                className="text-blue-600 text-sm"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(s.id)}
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
