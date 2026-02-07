import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import './PurchaseEvents.css';

const PurchaseEvents = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    try {
      const response = await api.get('/events/');
      setEvents(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load events. Please try again.');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES'
    }).format(price);
  };

  if (loading) {
    return (
      <div className="purchase-events-container">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>Loading events...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="purchase-events-container">
        <div className="error-message">
          <h3>Error Loading Events</h3>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadEvents}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const availableEvents = events.filter(event => event.available_tickets > 0);

  return (
    <div className="purchase-events-container">
      <div className="purchase-header">
        <h2>Available Events</h2>
        <p>Browse and purchase tickets for upcoming events</p>
      </div>

      {availableEvents.length === 0 ? (
        <div className="no-events">
          <h3>No Events Available</h3>
          <p>There are currently no events with available tickets.</p>
          <p>Check back later for new events!</p>
        </div>
      ) : (
        <div className="events-grid">
          {availableEvents.map(event => (
            <div key={event.id} className="event-card">
              <div className="event-image">
                <div className="event-image-placeholder">
                  <i className="fas fa-calendar-alt"></i>
                </div>
              </div>
              <div className="event-content">
                <h3 className="event-title">{event.name}</h3>
                <p className="event-description">{event.description}</p>
                
                <div className="event-details">
                  <div className="detail-item">
                    <i className="fas fa-clock"></i>
                    <span>{formatDate(event.date)}</span>
                  </div>
                  <div className="detail-item">
                    <i className="fas fa-map-marker-alt"></i>
                    <span>{event.location}</span>
                  </div>
                  <div className="detail-item">
                    <i className="fas fa-ticket-alt"></i>
                    <span>{event.available_tickets} tickets available</span>
                  </div>
                </div>

                <div className="event-footer">
                  <div className="event-price">
                    <span className="price-label">Price:</span>
                    <span className="price-value">{formatPrice(event.ticket_price)}</span>
                  </div>
                  <Link 
                    to={`/purchase/${event.id}`} 
                    className="btn btn-primary purchase-btn"
                  >
                    Purchase Ticket
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PurchaseEvents;






