import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Members from './pages/Members';
import Events from './pages/Events';
import Donations from './pages/Donations';
import Sacraments from './pages/Sacraments';
import Districts from './pages/Districts';
import Announcements from './pages/Announcements';


function App() {
  return (
    <Router>
      <nav>
        <Link to="/members">Members</Link> | 
        <Link to="/events">Events</Link> | 
        <Link to="/donations">Donations</Link> | 
        <Link to="/sacraments">Sacraments</Link> | 
        <Link to="/districts">Districts</Link> |
        <Link to="/announcements">Announcements</Link>
      </nav>
      <Routes>
        <Route path="/members" element={<Members />} />
        <Route path="/events" element={<Events />} />
        <Route path="/donations" element={<Donations />} />
        <Route path="/sacraments" element={<Sacraments />} />
        <Route path="/announcements" element={<Announcements />} />
        <Route path="/districts" element={<Districts />} />
      </Routes>
    </Router>
  );
}

export default App;
