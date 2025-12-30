import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  return (
    <>
      {/* NAVBAR */}
      <nav className="sticky top-0 z-50 bg-white border-b border-[#EFE7C9]">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          {/* Logo */}
          <Link to="/" className="text-xl font-semibold tracking-tight">
            St. Michael Church
          </Link>

          {/* Links */}
          <div className="flex items-center gap-6 text-sm font-medium">
            <Link to="/" className="hover:text-[#C6A44A]">
              Announcements
            </Link>

            {user && (
              <>
                <Link to="/events" className="hover:text-[#C6A44A]">
                  Events
                </Link>
                <Link to="/sacraments" className="hover:text-[#C6A44A]">
                  Sacraments
                </Link>
                <Link to="/donations" className="hover:text-[#C6A44A]">
                  Donations
                </Link>
              </>
            )}

            {/* Admin-only */}
            {user?.role === "admin" && (
              <>
                <Link to="/members" className="hover:text-[#C6A44A]">
                  Members
                </Link>
                <Link to="/districts" className="hover:text-[#C6A44A]">
                  Districts
                </Link>
              </>
            )}

            {/* Show user role badge */}
            {user && user.role && (
              <span className="px-3 py-1 text-xs rounded-full bg-[#FAF6E8] text-[#C6A44A] font-medium">
                {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
              </span>
            )}

            {/* Link Profile Button for unlinked users */}
            {user && !user.member_id && user.role !== 'admin' && (
              <Link
                to="/link-profile"
                className="px-3 py-1 text-xs rounded-full border border-[#C6A44A] text-[#C6A44A] hover:bg-[#FAF6E8]"
              >
                Link Profile
              </Link>
            )}

            {/* Auth */}
            {!user ? (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-full border hover:bg-[#FAF6E8]"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-2 rounded-full bg-[#C6A44A] text-white"
                >
                  Register
                </Link>
              </>
            ) : (
              <button
                onClick={() => {
                  logout();
                  navigate("/login");
                }}
                className="px-4 py-2 rounded-full border text-red-500 hover:bg-red-50"
              >
                Logout
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* PAGE CONTENT */}
      <main>{children}</main>
    </>
  );
}