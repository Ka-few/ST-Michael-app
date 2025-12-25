import { BrowserRouter, Routes, Route } from "react-router-dom";
import Announcements from "./pages/Announcements";
import Members from "./pages/Members";
import Events from "./pages/Events";
import Donations from "./pages/Donations";
import Sacraments from "./pages/Sacraments";
import Districts from "./pages/Districts";
import Layout from "./components/Layout";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Announcements />} />
          <Route path="/members" element={<Members />} />
          <Route path="/events" element={<Events />} />
          <Route path="/donations" element={<Donations />} />
          <Route path="/sacraments" element={<Sacraments />} />
          <Route path="/districts" element={<Districts />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
