import { useEffect, useMemo, useState } from "react";
import api from "../api/api";
import type { Member } from "../type/models";
import { Page, Card } from "../components/ui";

const PAGE_SIZE = 6;

export default function Members() {
  const [members, setMembers] = useState<Member[]>([]);
  const [form, setForm] = useState({
    name: "",
    contact: "",
    address: "",
    family: "",
    status: "active",
  });
  const [editId, setEditId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  // 🔍 Search & pagination state
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  // ================= FETCH =================
  const fetchMembers = () => {
    setLoading(true);
    api
      .get("/members/")
      .then(res => setMembers(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchMembers();
  }, []);

  // ================= FILTER =================
  const filteredMembers = useMemo(() => {
    const q = search.toLowerCase();
    return members.filter(m =>
      m.name.toLowerCase().includes(q) ||
      m.contact.toLowerCase().includes(q) ||
      (m.family || "").toLowerCase().includes(q)
    );
  }, [members, search]);

  // ================= PAGINATION =================
  const totalPages = Math.ceil(filteredMembers.length / PAGE_SIZE);

  const paginatedMembers = useMemo(() => {
    const start = (page - 1) * PAGE_SIZE;
    return filteredMembers.slice(start, start + PAGE_SIZE);
  }, [filteredMembers, page]);

  useEffect(() => {
    setPage(1); // reset page on search
  }, [search]);

  // ================= FORM =================
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const action = editId
      ? api.put(`/members/${editId}`, form)
      : api.post("/members/", form);

    action.then(() => {
      fetchMembers();
      setForm({
        name: "",
        contact: "",
        address: "",
        family: "",
        status: "active",
      });
      setEditId(null);
    });
  };

  // ================= ACTIONS =================
  const handleEdit = (m: Member) => {
    setForm({
      name: m.name,
      contact: m.contact,
      address: m.address || "",
      family: m.family || "",
      status: m.status || "active",
    });
    setEditId(m.id);
  };

  const handleDelete = (id: number) => {
    if (window.confirm("Remove this member?")) {
      api.delete(`/members/${id}`).then(fetchMembers);
    }
  };

  // ================= UI =================
  return (
    <Page title="Parish Members">
      {/* FORM */}
      <Card className="mb-8">
        <form onSubmit={handleSubmit} className="grid md:grid-cols-5 gap-4">
          <input
            name="name"
            value={form.name}
            onChange={handleChange}
            className="border rounded-lg px-3 py-2"
            placeholder="Full Name"
            required
          />
          <input
            name="contact"
            value={form.contact}
            onChange={handleChange}
            className="border rounded-lg px-3 py-2"
            placeholder="Phone"
            required
          />
          <input
            name="address"
            value={form.address}
            onChange={handleChange}
            className="border rounded-lg px-3 py-2"
            placeholder="Address"
          />
          <input
            name="family"
            value={form.family}
            onChange={handleChange}
            className="border rounded-lg px-3 py-2"
            placeholder="Family"
          />
          <button
            type="submit"
            className="bg-[#C6A44A] text-white rounded-lg px-4 py-2 hover:bg-[#B8961E]"
          >
            {editId ? "Update" : "Add"}
          </button>
        </form>
      </Card>

      {/* SEARCH */}
      <div className="mb-6 flex justify-between items-center">
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search members..."
          className="w-full md:w-1/3 border rounded-xl px-4 py-2"
        />
        <span className="text-sm text-gray-500 ml-4">
          {filteredMembers.length} members
        </span>
      </div>

      {/* LIST */}
      {loading ? (
        <p>Loading members...</p>
      ) : (
        <>
          <div className="grid md:grid-cols-3 gap-6">
            {paginatedMembers.map(m => (
              <Card key={m.id}>
                <h3 className="text-lg font-semibold">{m.name}</h3>
                <p className="text-sm text-gray-500">{m.contact}</p>
                <p className="text-sm text-gray-400">{m.address}</p>

                <span
                  className={`
                    inline-block mt-3 px-3 py-1 text-xs rounded-full
                    ${
                      m.status === "active"
                        ? "bg-[#FAF6E8] text-[#9C7F2E]"
                        : "bg-gray-200 text-gray-600"
                    }
                  `}
                >
                  {m.status}
                </span>

                <div className="flex gap-4 mt-6 text-sm">
                  <button
                    onClick={() => handleEdit(m)}
                    className="text-[#C6A44A] hover:underline"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(m.id)}
                    className="text-red-500 hover:underline"
                  >
                    Remove
                  </button>
                </div>
              </Card>
            ))}
          </div>

          {/* PAGINATION */}
          {totalPages > 1 && (
            <div className="flex justify-center gap-2 mt-10">
              {Array.from({ length: totalPages }).map((_, i) => (
                <button
                  key={i}
                  onClick={() => setPage(i + 1)}
                  className={`px-4 py-2 rounded-lg text-sm ${
                    page === i + 1
                      ? "bg-[#C6A44A] text-white"
                      : "bg-white border hover:bg-[#FAF6E8]"
                  }`}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          )}
        </>
      )}
    </Page>
  );
}
