import { useEffect, useState } from 'react';
import api from '../api/api';
import type { Event } from '../type/models';
import { useAuth } from '../context/AuthContext';


export default function Events() {
  const { user } = useAuth();
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);

  const [form, setForm] = useState({ name: '', description: '', date: '' });
  const [editId, setEditId] = useState<number | null>(null);

  const fetchEvents = () => {
    setLoading(true);
    api.get('/events/')
      .then(res => setEvents(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => fetchEvents(), []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editId) {
      api.put(`/events/${editId}`, form).then(() => {
        fetchEvents();
        setForm({ name: '', description: '', date: '' });
        setEditId(null);
      });
    } else {
      api.post('/events/', form).then(() => {
        fetchEvents();
        setForm({ name: '', description: '', date: '' });
      });
    }
  };

  const handleEdit = (e: Event) => {
    setForm({ name: e.name, description: e.description || '', date: e.date });
    setEditId(e.id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Delete this event?')) api.delete(`/events/${id}`).then(fetchEvents);
  };

  const isAdmin = user?.role === 'admin';

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-[#C9A227] mb-6">Church Events</h1>

      {isAdmin && (
        <div className="bg-white p-6 rounded-xl shadow border border-[#E6D8A3] mb-8">
          <form
            onSubmit={handleSubmit}
            className="grid md:grid-cols-4 gap-4"
          >
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              className="border rounded-lg px-3 py-2"
              placeholder="Event Name"
              required
            />

            <input
              name="date"
              type="date"
              value={form.date}
              onChange={handleChange}
              className="border rounded-lg px-3 py-2"
              required
            />

            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              className="border rounded-lg px-3 py-2 md:col-span-2"
              placeholder="Description"
            />

            <button
              type="submit"
              className="bg-[#C9A227] text-white rounded-lg px-4 py-2 hover:bg-[#B8961E]"
            >
              {editId ? "Update Event" : "Add Event"}
            </button>
          </form>
        </div>
      )}

      {loading ? (
        <p>Loading events...</p>
      ) : (
        <div className="grid md:grid-cols-3 gap-6">
          {events.map(event => (
            <div
              key={event.id}
              className="bg-white p-4 rounded-xl shadow border"
            >
              <h3 className="font-semibold">{event.name}</h3>
              <p className="text-sm text-gray-600">{event.description}</p>
              <p className="text-sm text-gray-500">{event.date}</p>

              {isAdmin && (
                <div className="flex gap-3 mt-3">
                  <button
                    onClick={() => handleEdit(event)}
                    className="text-blue-600 text-sm"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(event.id)}
                    className="text-red-600 text-sm"
                  >
                    Delete
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
