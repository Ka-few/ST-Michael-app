import { useEffect, useState } from 'react';
import api from '../api/api';
import type { Attendance } from '../type/models';



export default function Attendance() {
  const [records, setRecords] = useState<Attendance[]>([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({ event_id: '', member_id: '', status: 'present' });
  const [editId, setEditId] = useState<number | null>(null);

  const fetchRecords = () => {
    setLoading(true);
    api.get('/attendance/')
      .then(res => setRecords(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => fetchRecords(), []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = { ...form, event_id: Number(form.event_id), member_id: Number(form.member_id) };
    if (editId) {
      api.put(`/attendance/${editId}`, payload).then(() => {
        fetchRecords();
        setForm({ event_id: '', member_id: '', status: 'present' });
        setEditId(null);
      });
    } else {
      api.post('/attendance/', payload).then(() => {
        fetchRecords();
        setForm({ event_id: '', member_id: '', status: 'present' });
      });
    }
  };

  const handleEdit = (a: Attendance) => {
    setForm({ event_id: String(a.event_id), member_id: String(a.member_id), status: a.status });
    setEditId(a.id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Delete this record?')) api.delete(`/attendance/${id}`).then(fetchRecords);
  };

  return (
    <div>
      <h1>Attendance</h1>

      <form onSubmit={handleSubmit}>
        <input name="event_id" value={form.event_id} onChange={handleChange} placeholder="Event ID" required />
        <input name="member_id" value={form.member_id} onChange={handleChange} placeholder="Member ID" required />
        <select name="status" value={form.status} onChange={handleChange}>
          <option value="present">Present</option>
          <option value="absent">Absent</option>
        </select>
        <button type="submit">{editId ? 'Update' : 'Add'} Attendance</button>
      </form>

      {loading ? <p>Loading...</p> : (
        <ul>
          {records.map(a => (
            <li key={a.id}>
              {a.member_name} - {a.event_name} ({a.status})
              <button onClick={() => handleEdit(a)}>Edit</button>
              <button onClick={() => handleDelete(a.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
