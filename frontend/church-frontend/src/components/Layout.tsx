import { NavLink } from "react-router-dom";

const navItems = [
  { name: "Home", path: "/" },
  { name: "Members", path: "/members" },
  { name: "Districts", path: "/districts" },
  { name: "Events", path: "/events" },
  { name: "Sacraments", path: "/sacraments" },
  { name: "Donations", path: "/donations" },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-[#FAF9F6]">
      {/* Top Bar */}
      <header className="bg-white border-b border-[#EFE7C9] shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-[#1F2937]">
              St. Michael Parish
            </h1>
            <p className="text-xs text-[#C6A44A] tracking-wide">
              Parish Management System
            </p>
          </div>

          <nav className="flex gap-6">
            {navItems.map(item => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `text-sm font-medium transition ${
                    isActive
                      ? "text-[#C6A44A]"
                      : "text-gray-600 hover:text-[#C6A44A]"
                  }`
                }
              >
                {item.name}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      {/* Page Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
    </div>
  );
}
