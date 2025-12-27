import type { Member } from "../type/models";

interface Props {
  member: Member | null;
  onClose: () => void;
  onEdit: (member: Member) => void;
  onDelete: (id: number) => void;
}

export default function MemberDrawer({
  member,
  onClose,
  onEdit,
  onDelete,
}: Props) {
  if (!member) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      {/* Overlay */}
      <div
        className="flex-1 bg-black/40 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Drawer */}
      <div className="w-full sm:w-[420px] bg-white shadow-2xl p-6 overflow-y-auto animate-slide-in">
        {/* Header */}
        <div className="flex justify-between items-center border-b pb-4 mb-6">
          <h2 className="text-xl font-semibold text-gray-800">
            Member Profile
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-700 text-xl"
          >
            ×
          </button>
        </div>

        {/* Avatar */}
        <div className="flex items-center gap-4 mb-6">
          <div className="h-16 w-16 rounded-full bg-[#FAF6E8] flex items-center justify-center text-[#9C7F2E] font-bold text-xl">
            {member.name.charAt(0)}
          </div>
          <div>
            <h3 className="text-lg font-semibold">{member.name}</h3>
            <p className="text-sm text-gray-500">{member.contact}</p>
          </div>
        </div>

        {/* Details */}
        <div className="space-y-4 text-sm">
          <Detail label="Address" value={member.address || "—"} />
          <Detail label="Family" value={member.family || "—"} />

          <div>
            <span className="text-gray-400 block mb-1">Status</span>
            <span
              className={`inline-block px-3 py-1 rounded-full text-xs
                ${
                  member.status === "active"
                    ? "bg-[#FAF6E8] text-[#9C7F2E]"
                    : "bg-gray-200 text-gray-600"
                }
              `}
            >
              {member.status}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="mt-10 flex gap-3">
          <button
            onClick={() => onEdit(member)}
            className="flex-1 bg-[#C6A44A] text-white py-2 rounded-lg hover:bg-[#B8961E]"
          >
            Edit Member
          </button>

          <button
            onClick={() => onDelete(member.id)}
            className="flex-1 border border-red-500 text-red-500 py-2 rounded-lg hover:bg-red-50"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <span className="text-gray-400 block mb-1">{label}</span>
      <p className="text-gray-700 font-medium">{value}</p>
    </div>
  );
}
