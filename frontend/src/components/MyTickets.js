import React, { useEffect, useState } from 'react';
import api from '../services/api';
import './MyTickets.css';

const MyTickets = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      setLoading(true);
      const response = await api.get('/payments/my-tickets/');
      setTickets(response.data);
      setError('');
    } catch (err) {
      console.error('Error loading tickets:', err);
      if (err.response?.status === 401) {
        setError('Please login to view your tickets');
      } else {
        setError('Failed to load tickets. Please try again.');
      }
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

  const getStatusBadge = (paymentStatus, isValidated) => {
    if (paymentStatus === 'completed') {
      return <span className="badge bg-success">Paid</span>;
    } else if (paymentStatus === 'pending') {
      return <span className="badge bg-warning">Pending</span>;
    } else if (paymentStatus === 'failed') {
      return <span className="badge bg-danger">Failed</span>;
    }
    return <span className="badge bg-secondary">Unknown</span>;
  };

  const getValidationBadge = (isValidated) => {
    if (isValidated) {
      return <span className="badge bg-success">Validated</span>;
    } else {
      return <span className="badge bg-secondary">Not Validated</span>;
    }
  };

  if (loading) {
    return (
      <div className="my-tickets-container">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>Loading your tickets...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="my-tickets-container">
        <div className="error-message">
          <h3>Error Loading Tickets</h3>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadTickets}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="my-tickets-container">
      <div className="tickets-header">
        <h2>My Tickets</h2>
        <p>View and manage your purchased tickets</p>
      </div>

      {tickets.length === 0 ? (
        <div className="no-tickets">
          <div className="no-tickets-icon">
            <i className="fas fa-ticket-alt"></i>
          </div>
          <h3>No Tickets Found</h3>
          <p>You haven't purchased any tickets yet.</p>
          <a href="/purchase" className="btn btn-primary">
            Browse Events
          </a>
        </div>
      ) : (
        <div className="tickets-grid">
          {tickets.map(ticket => (
            <div key={ticket.id} className="ticket-card">
              <div className="ticket-header">
                <h3>{ticket.event_name}</h3>
                <div className="ticket-badges">
                  {getStatusBadge(ticket.payment_status, ticket.is_validated)}
                  {getValidationBadge(ticket.is_validated)}
                </div>
              </div>
              
              <div className="ticket-details">
                <div className="detail-item">
                  <i className="fas fa-calendar"></i>
                  <span>{formatDate(ticket.event_date)}</span>
                </div>
                <div className="detail-item">
                  <i className="fas fa-map-marker-alt"></i>
                  <span>{ticket.event_location}</span>
                </div>
                <div className="detail-item">
                  <i className="fas fa-clock"></i>
                  <span>Purchased: {formatDate(ticket.purchase_date)}</span>
                </div>
                <div className="detail-item">
                  <i className="fas fa-hashtag"></i>
                  <span>Ticket ID: {ticket.unique_code}</span>
                </div>
              </div>

              <div className="ticket-actions">
                <button 
                  className="btn btn-outline-primary btn-sm"
                  onClick={() => navigator.clipboard.writeText(ticket.unique_code)}
                  title="Copy Ticket ID"
                >
                  <i className="fas fa-copy"></i> Copy ID
                </button>
                {ticket.payment_status === 'completed' && (
                  <button 
                    className="btn btn-outline-success btn-sm"
                    title="Download Ticket"
                  >
                    <i className="fas fa-download"></i> Download
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyTickets;