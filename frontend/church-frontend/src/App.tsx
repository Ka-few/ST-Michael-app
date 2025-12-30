import { Routes, Route, Navigate } from "react-router-dom";
import Announcements from "./pages/Announcements";
import Members from "./pages/Members";
import Events from "./pages/Events";
import Donations from "./pages/Donations";
import Sacraments from "./pages/Sacraments";
import Districts from "./pages/Districts";
import Login from "./pages/Login";
import Register from "./pages/Register";
import LinkProfile from "./pages/LinkProfile";
import Layout from "./components/Layout";
import ProtectedRoute from "./routes/ProtectedRoute";
import { useAuth } from "./context/AuthContext";

export default function App() {
  const { user } = useAuth();

  return (
    <Layout>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={user ? <Navigate to="/" replace /> : <Login />} />
        <Route path="/register" element={user ? <Navigate to="/" replace /> : <Register />} />

        {/* Shared Routes (All authenticated users) */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Announcements />
            </ProtectedRoute>
          }
        />

        <Route
          path="/events"
          element={
            <ProtectedRoute>
              <Events />
            </ProtectedRoute>
          }
        />

        <Route
          path="/donations"
          element={
            <ProtectedRoute>
              <Donations />
            </ProtectedRoute>
          }
        />

        <Route
          path="/sacraments"
          element={
            <ProtectedRoute>
              <Sacraments />
            </ProtectedRoute>
          }
        />

        <Route
          path="/link-profile"
          element={
            <ProtectedRoute>
              <LinkProfile />
            </ProtectedRoute>
          }
        />

        {/* Admin-Only Routes */}
        <Route
          path="/members"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Members />
            </ProtectedRoute>
          }
        />

        <Route
          path="/districts"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Districts />
            </ProtectedRoute>
          }
        />

        {/* Catch all - redirect to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}