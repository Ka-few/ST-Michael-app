import { useEffect, useState } from "react";
import type { ChangeEvent } from "react";
import {
  getDistricts,
  createDistrict,
  updateDistrict,
  deleteDistrict,
} from "../services/districts";
import { Page, Card, PrimaryButton, Input } from "../components/ui";

export default function Districts() {
  const [districts, setDistricts] = useState<any[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState({ name: "", leader_name: "" });

  const load = async () => setDistricts(await getDistricts());
  useEffect(() => { load(); }, []);

  const handleSave = async (id?: number) => {
    if (id) {
      await updateDistrict(id, form);
      setEditingId(null);
    } else {
      await createDistrict(form);
    }
    setForm({ name: "", leader_name: "" });
    load();
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this district?")) {
      await deleteDistrict(id);
      load();
    }
  };

  return (
    <Page title="Church Districts">
      <Card>
        <div className="grid md:grid-cols-3 gap-4">
          <Input
            placeholder="District name"
            value={form.name}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setForm({ ...form, name: e.target.value })}
          />
          <Input
            placeholder="Leader name"
            value={form.leader_name}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setForm({ ...form, leader_name: e.target.value })}
          />
          <PrimaryButton onClick={() => handleSave()}>
            Add District
          </PrimaryButton>
        </div>
      </Card>

      <div className="grid md:grid-cols-3 gap-6">
        {districts.map(d => (
          <Card key={d.id}>
            {editingId === d.id ? (
              <>
                <Input
                  value={form.name}
                  onChange={(e: ChangeEvent<HTMLInputElement>) => setForm({ ...form, name: e.target.value })}
                />
                <Input
                  value={form.leader_name}
                  onChange={(e: ChangeEvent<HTMLInputElement>) =>
                    setForm({ ...form, leader_name: e.target.value })
                  }
                />
                <PrimaryButton onClick={() => handleSave(d.id)}>
                  Save
                </PrimaryButton>
              </>
            ) : (
              <>
                <h3 className="text-lg font-semibold">{d.name}</h3>
                <p className="text-sm text-gray-500">
                  Leader: {d.leader_name || "—"}
                </p>

                <div className="flex gap-3 mt-4">
                  <button
                    onClick={() => {
                      setEditingId(d.id);
                      setForm({ name: d.name, leader_name: d.leader_name || "" });
                    }}
                    className="text-[#C6A44A] font-medium"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(d.id)}
                    className="text-red-500 font-medium"
                  >
                    Delete
                  </button>
                </div>
              </>
            )}
          </Card>
        ))}
      </div>
    </Page>
  );
}
