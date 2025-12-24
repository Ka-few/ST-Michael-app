import { useEffect, useState } from "react";
import type { ChangeEvent } from "react";
import { getDistricts, createDistrict } from "../services/districts";
import { Page, Card, PrimaryButton, Input } from "../components/ui";

export default function Districts() {
  const [districts, setDistricts] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [leader, setLeader] = useState("");

  const loadDistricts = async () => {
    const data = await getDistricts();
    setDistricts(data);
  };

  useEffect(() => {
    loadDistricts();
  }, []);

  const handleCreate = async () => {
    if (!name) return;
    await createDistrict({ name, leader_name: leader });
    setName("");
    setLeader("");
    loadDistricts();
  };

  return (
    <Page title="Church Districts">
      <Card>
        <div className="grid md:grid-cols-3 gap-4">
          <Input
            placeholder="District name"
            value={name}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
          />
          <Input
            placeholder="Leader name"
            value={leader}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setLeader(e.target.value)}
          />
          <PrimaryButton onClick={handleCreate}>
            Add District
          </PrimaryButton>
        </div>
      </Card>

      <div className="grid md:grid-cols-3 gap-6">
        {districts.map(d => (
          <Card key={d.id}>
            <h3 className="text-lg font-semibold">{d.name}</h3>
            <p className="text-sm text-gray-500">
              Leader: {d.leader_name || "—"}
            </p>
            <p className="mt-3 text-[#C6A44A] font-medium">
              {d.member_count} Members
            </p>
          </Card>
        ))}
      </div>
    </Page>
  );
}
