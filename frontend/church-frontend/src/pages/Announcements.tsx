import React, { useEffect, useState } from "react";
import {
  getAnnouncements,
  createAnnouncement,
} from "../services/announcements";
import { Page, Card, PrimaryButton, Input } from "../components/ui";

export default function Announcements() {
  const [announcements, setAnnouncements] = useState<any[]>([]);
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");

  const loadAnnouncements = async () => {
    const data = await getAnnouncements();
    setAnnouncements(data);
  };

  useEffect(() => {
    loadAnnouncements();
  }, []);

  const handleCreate = async () => {
    if (!title || !message) return;
    await createAnnouncement({
      title,
      message,
      category: "general",
    });
    setTitle("");
    setMessage("");
    loadAnnouncements();
  };

  return (
    <Page title="Parish Announcements">
      <Card>
        <div className="space-y-4">
          <Input
            placeholder="Announcement title"
            value={title}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
          />
          <textarea
            className="w-full rounded-xl border border-[#EFE7C9] p-4"
            rows={4}
            placeholder="Announcement message"
            value={message}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setMessage(e.target.value)}
          />
          <PrimaryButton onClick={handleCreate}>
            Publish Announcement
          </PrimaryButton>
        </div>
      </Card>

      <div className="space-y-6">
        {announcements.map(a => (
          <Card key={a.id}>
            <h3 className="text-lg font-semibold">{a.title}</h3>
            <p className="text-sm text-gray-500 mb-2">
              {a.category?.toUpperCase()}
            </p>
            <p className="text-gray-700 leading-relaxed">
              {a.message}
            </p>
          </Card>
        ))}
      </div>
    </Page>
  );
}
