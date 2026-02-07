import { Route, Routes } from 'react-router-dom';
import Navigation from './components/Navigation';
import EventList from './components/EventList';
import EventDetail from './components/EventDetail';
import TicketPurchase from './components/TicketPurchase';
import MyTickets from './components/MyTickets';
import Login from './components/Login';
import Register from './components/Register';
import AdminEventManager from './components/AdminEventManager';
import AdminProtected from './components/AdminProtected';
import PurchaseEvents from './components/PurchaseEvents';

function App() {
  return (
    <div className="App">
      <Navigation />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<EventList />} />
        <Route path="/purchase" element={<PurchaseEvents />} />
        <Route path="/events/:id" element={<EventDetail />} />
        <Route path="/purchase/:id" element={<TicketPurchase />} />
        <Route path="/my-tickets" element={<MyTickets />} />
        <Route 
          path="/admin/events" 
          element={
            <AdminProtected>
              <AdminEventManager />
            </AdminProtected>
          } 
        />
      </Routes>
    </div>
  );
}

export default App; 