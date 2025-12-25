import { useEffect, useState } from "react";
import type { ChangeEvent } from "react";
import {
  getAnnouncements,
  createAnnouncement,
  updateAnnouncement,
  deleteAnnouncement,
} from "../services/announcements";
import { Page, Card, PrimaryButton, Input } from "../components/ui";

export default function Announcements() {
  const [announcements, setAnnouncements] = useState<any[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [form, setForm] = useState({ title: "", message: "" });

  const load = async () => setAnnouncements(await getAnnouncements());
  useEffect(() => {
    load();
  }, []);

  const handleSave = async (id?: number) => {
    if (!form.title || !form.message) return;

    if (id) {
      await updateAnnouncement(id, form);
      setEditingId(null);
    } else {
      await createAnnouncement({ ...form, category: "general" });
    }

    setForm({ title: "", message: "" });
    load();
  };

  const handleDelete = async (id: number) => {
    if (confirm("Delete this announcement?")) {
      await deleteAnnouncement(id);
      load();
    }
  };

  return (
    <Page title="Announcements">
      {/* Page Intro */}
      <div className="mb-10">
        <h2 className="text-3xl font-semibold text-gray-800">
          Parish Announcements
        </h2>
        <p className="text-gray-500 mt-1 max-w-2xl">
          Official parish notices, updates, and important information for the
          church community.
        </p>
      </div>

      {/* Create Announcement */}
      <Card className="mb-12">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Publish New Announcement
        </h3>

        <Input
          placeholder="Announcement title"
          value={form.title}
          onChange={(e: ChangeEvent<HTMLInputElement>) =>
            setForm({ ...form, title: e.target.value })
          }
        />

        <textarea
          className="w-full rounded-xl border border-[#EFE7C9] p-4 mt-4 text-sm leading-relaxed focus:ring-2 focus:ring-[#C6A44A] outline-none"
          rows={5}
          placeholder="Write the announcement message..."
          value={form.message}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
            setForm({ ...form, message: e.target.value })
          }
        />

        <PrimaryButton className="mt-4" onClick={() => handleSave()}>
          Publish Announcement
        </PrimaryButton>
      </Card>

      {/* Announcement Feed */}
      <div className="space-y-6">
        {announcements.length === 0 && (
          <Card>
            <p className="text-gray-500 text-sm">
              No announcements have been published yet.
            </p>
          </Card>
        )}

        {announcements.map((a) => (
          <Card key={a.id}>
            {editingId === a.id ? (
              <>
                <Input
                  value={form.title}
                  onChange={(e: ChangeEvent<HTMLInputElement>) =>
                    setForm({ ...form, title: e.target.value })
                  }
                />

                <textarea
                  className="w-full rounded-xl border border-[#EFE7C9] p-4 mt-4 text-sm leading-relaxed"
                  rows={5}
                  value={form.message}
                  onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
                    setForm({ ...form, message: e.target.value })
                  }
                />

                <div className="flex gap-4 mt-4">
                  <PrimaryButton onClick={() => handleSave(a.id)}>
                    Save Changes
                  </PrimaryButton>
                  <button
                    className="text-sm text-gray-500"
                    onClick={() => setEditingId(null)}
                  >
                    Cancel
                  </button>
                </div>
              </>
            ) : (
              <>
                {/* Label */}
                <p className="text-xs uppercase tracking-wide text-[#C6A44A] mb-2">
                  Parish Notice
                </p>

                {/* Title */}
                <h3 className="text-xl font-semibold text-gray-800">
                  {a.title}
                </h3>

                {/* Message */}
                <p className="text-gray-700 mt-3 leading-relaxed">
                  {a.message}
                </p>

                {/* Footer */}
                <div className="flex items-center justify-between mt-6">
                  <span className="text-xs text-gray-400">
                    Posted on{" "}
                    {a.created_at
                      ? new Date(a.created_at).toLocaleDateString()
                      : ""}
                  </span>

                  <div className="flex gap-4">
                    <button
                      className="text-sm font-medium text-[#C6A44A]"
                      onClick={() => {
                        setEditingId(a.id);
                        setForm({
                          title: a.title,
                          message: a.message,
                        });
                      }}
                    >
                      Edit
                    </button>
                    <button
                      className="text-sm font-medium text-red-500"
                      onClick={() => handleDelete(a.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </>
            )}
          </Card>
        ))}
      </div>
    </Page>
  );
}
