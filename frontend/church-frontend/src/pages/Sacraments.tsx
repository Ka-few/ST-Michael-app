import { useEffect, useState } from 'react';
import api from '../api/api';
import { useAuth } from '../context/AuthContext';

interface Sacrament {
  id: number;
  user_id?: number;
  type: string;
  date: string | null;
  notes?: string;
}

export default function Sacraments() {
  const { user, token } = useAuth();
  const [sacraments, setSacraments] = useState<Sacrament[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [form, setForm] = useState({
    user_id: '',
    type: '',
    date: '',
    notes: ''
  });
  const [editId, setEditId] = useState<number | null>(null);

  const fetchSacraments = () => {
    // Don't fetch if no token
    if (!token) {
      console.log('⏳ No token available, skipping fetch');
      setLoading(false);
      return;
    }

    console.log('📋 Fetching sacraments for role:', user?.role);
    setLoading(true);
    setError('');

    // Admin gets all sacraments, members get their own
    const endpoint = user?.role === 'admin' ? '/sacraments/admin/all' : '/sacraments/';

    api.get(endpoint)
      .then(res => {
        console.log('✅ Sacraments loaded:', res.data.length, 'records');
        setSacraments(res.data);
      })
      .catch(err => {
        console.error('❌ Error fetching sacraments:', err);
        setError(err.response?.data?.error || 'Failed to load sacraments');
      })
      .finally(() => setLoading(false));
  };

  // Only fetch when token is available
  useEffect(() => {
    if (token && user) {
      fetchSacraments();
    } else {
      setLoading(false);
    }
  }, [user, token]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Admin can create for any user, members create for themselves
    const payload = user?.role === 'admin'
      ? { ...form, user_id: Number(form.user_id) }
      : { type: form.type, date: form.date, notes: form.notes };

    if (editId) {
      // Update sacrament
      const endpoint = user?.role === 'admin' ? `/sacraments/${editId}` : `/sacraments/${editId}`;
      console.log('✏️ Updating sacrament:', editId);
      api.put(endpoint, payload)
        .then(() => {
          console.log('✅ Sacrament updated');
          fetchSacraments();
          setForm({ user_id: '', type: '', date: '', notes: '' });
          setEditId(null);
        })
        .catch(err => {
          console.error('❌ Update failed:', err);
          setError(err.response?.data?.error || 'Failed to update');
        });
    } else {
      // Create new sacrament
      const endpoint = user?.role === 'admin' ? '/sacraments/admin/add' : '/sacraments/';
      console.log('➕ Creating sacrament:', payload);
      api.post(endpoint, payload)
        .then(() => {
          console.log('✅ Sacrament created');
          fetchSacraments();
          setForm({ user_id: '', type: '', date: '', notes: '' });
        })
        .catch(err => {
          console.error('❌ Create failed:', err);
          setError(err.response?.data?.error || 'Failed to create');
        });
    }
  };

  const handleEdit = (s: Sacrament) => {
    setForm({
      user_id: String(s.user_id || ''),
      type: s.type,
      date: s.date || '',
      notes: s.notes || ''
    });
    setEditId(s.id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm('Delete this sacrament?')) {
      const endpoint = user?.role === 'admin' ? `/sacraments/admin/${id}` : `/sacraments/${id}`;
      console.log('🗑️ Deleting sacrament:', id);
      api.delete(endpoint)
        .then(() => {
          console.log('✅ Sacrament deleted');
          fetchSacraments();
        })
        .catch(err => {
          console.error('❌ Delete failed:', err);
          setError(err.response?.data?.error || 'Failed to delete');
        });
    }
  };

  // Show message if not authenticated
  if (!token) {
    return (
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <h2 className="text-xl font-semibold text-yellow-800 mb-2">
            Authentication Required
          </h2>
          <p className="text-yellow-600">
            Please log in to view sacraments.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-8">
      <h1 className="text-3xl font-bold mb-6">
        {user?.role === 'admin' ? 'Manage Sacraments' : 'My Sacraments Journey'}
      </h1>

      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-6">
          {error}
        </div>
      )}

      {/* Admin Only: Create/Edit Form */}
      {user?.role === 'admin' && (
        <div className="bg-white p-6 rounded-xl shadow border border-[#E6D8A3] mb-6">
          <h2 className="text-xl font-semibold text-[#C9A227] mb-4">
            {editId ? "Edit Sacrament" : "Add Sacrament"}
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">User ID</label>
              <input
                name="user_id"
                value={form.user_id}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                placeholder="User ID"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Sacrament Type</label>
              <select
                name="type"
                value={form.type}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                required
              >
                <option value="">Select Sacrament</option>
                <option value="Baptism">Baptism</option>
                <option value="Confirmation">Confirmation</option>
                <option value="Holy Communion">Holy Communion</option>
                <option value="Marriage">Marriage</option>
                <option value="Holy Orders">Holy Orders</option>
                <option value="Anointing of the Sick">Anointing of the Sick</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Date Received</label>
              <input
                name="date"
                type="date"
                value={form.date}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Notes (Optional)</label>
              <textarea
                name="notes"
                value={form.notes}
                onChange={handleChange}
                className="w-full border rounded-lg px-3 py-2"
                placeholder="Additional notes..."
                rows={3}
              />
            </div>

            <button
              type="submit"
              className="w-full bg-[#C9A227] text-white rounded-lg hover:bg-[#B8961E] px-4 py-2"
            >
              {editId ? "Update" : "Add"}
            </button>
          </form>
        </div>
      )}

      {loading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#C6A44A] mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading sacraments...</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sacraments.length === 0 ? (
            <p className="col-span-full text-center text-gray-500 py-8">
              No sacraments recorded yet.
            </p>
          ) : (
            sacraments.map(s => (
              <div
                key={s.id}
                className="border rounded-lg p-4 shadow-sm bg-white hover:shadow-md transition-shadow"
              >
                {user?.role === 'admin' && (
                  <p className="text-sm text-gray-500 mb-2">User #{s.user_id}</p>
                )}
                <p className="font-semibold text-lg text-[#C9A227]">
                  {s.type}
                </p>
                {s.date && (
                  <p className="text-sm text-gray-600 mt-1">
                    {new Date(s.date).toLocaleDateString()}
                  </p>
                )}
                {s.notes && (
                  <p className="text-sm text-gray-600 mt-2 italic">
                    {s.notes}
                  </p>
                )}

                {user?.role === 'admin' && (
                  <div className="flex gap-3 mt-4">
                    <button
                      onClick={() => handleEdit(s)}
                      className="text-blue-600 text-sm hover:underline"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(s.id)}
                      className="text-red-600 text-sm hover:underline"
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}