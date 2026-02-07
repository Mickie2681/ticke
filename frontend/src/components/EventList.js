import React, { useEffect, useState } from 'react';
import api from '../services/api';
import { Link, useNavigate } from 'react-router-dom';

const EventList = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        const response = await api.get('/events/');
        setEvents(response.data);
      } catch (error) {
        if (error.response?.status === 401) {
          setError('Please login to view events');
        } else {
          setError('Error loading events: ' + (error.response?.data?.error || 'Unknown error'));
        }
        console.error('Error fetching events:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  const handlePurchaseClick = (eventId) => {
    const token = localStorage.getItem('accessToken');
    if (!token) {
      alert('Please login to purchase tickets');
      navigate('/login');
      return;
    }
    navigate(`/purchase/${eventId}`);
  };

  if (loading) {
    return (
      <div className="container mt-5">
        <div className="text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Available Events</h1>
      {events.length === 0 ? (
        <div className="alert alert-info" role="alert">
          No events available at the moment.
        </div>
      ) : (
        <div className="row">
          {events.map(event => (
            <div key={event.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{event.name}</h5>
                  <p className="card-text">
                    <strong>Price:</strong> ${event.ticket_price}<br/>
                    <strong>Available Tickets:</strong> {event.available_tickets}<br/>
                    <strong>Date:</strong> {new Date(event.date).toLocaleDateString()}
                  </p>
                  <div className="d-grid gap-2">
                    <Link to={`/events/${event.id}`} className="btn btn-outline-primary">
                      View Details
                    </Link>
                    <button 
                      className="btn btn-success"
                      onClick={() => handlePurchaseClick(event.id)}
                    >
                      Purchase Ticket
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EventList;