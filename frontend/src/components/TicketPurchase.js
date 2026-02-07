import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import './TicketPurchase.css';

const TicketPurchase = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [event, setEvent] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [eventLoading, setEventLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const loadEventDetails = async () => {
    try {
      const response = await api.get(`/events/${id}/`);
      setEvent(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load event details. Please try again.');
      console.error('Error loading event:', err);
    } finally {
      setEventLoading(false);
    }
  };

  useEffect(() => {
    // Check if user is authenticated
    const token = localStorage.getItem('accessToken');
    if (!token) {
      alert('Please login to purchase tickets');
      navigate('/login');
      return;
    }

    // Load event details
    loadEventDetails();
  }, [id, navigate]);

  const handlePurchase = async (e) => {
    e.preventDefault();
    
    const token = localStorage.getItem('accessToken');
    if (!token) {
      alert('Please login to purchase tickets');
      navigate('/login');
      return;
    }

    // Validate phone number
    const fullPhoneNumber = phoneNumber.startsWith('254') ? phoneNumber : `254${phoneNumber}`;
    
    if (fullPhoneNumber.length !== 12) {
      setError('Phone number must be 12 digits (e.g., 254712345678)');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const response = await api.post('/payments/purchase/', { 
        event_id: id, 
        phone_number: fullPhoneNumber 
      });
      
      setSuccess('Payment initiated successfully! Check your phone for M-Pesa STK Push notification. Complete the payment to receive your ticket.');
      setPhoneNumber('');
      console.log('Purchase response:', response.data);
    } catch (error) {
      if (error.response?.status === 401) {
        alert('Authentication failed. Please login again.');
        localStorage.removeItem('accessToken');
        navigate('/login');
      } else {
        const errorMessage = error.response?.data?.error || 'Error initiating payment. Please try again.';
        setError(errorMessage);
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

  if (eventLoading) {
    return (
      <div className="ticket-purchase-container">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>Loading event details...</p>
        </div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="ticket-purchase-container">
        <div className="error-message">
          <h3>Event Not Found</h3>
          <p>The event you're looking for doesn't exist or has been removed.</p>
          <button className="btn btn-primary" onClick={() => navigate('/purchase')}>
            Browse Events
          </button>
        </div>
      </div>
    );
  }

  if (event.available_tickets <= 0) {
    return (
      <div className="ticket-purchase-container">
        <div className="error-message">
          <h3>Sold Out</h3>
          <p>Sorry, all tickets for this event have been sold out.</p>
          <button className="btn btn-primary" onClick={() => navigate('/purchase')}>
            Browse Other Events
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="ticket-purchase-container">
      <div className="purchase-card">
        <div className="event-details">
          <h2>Purchase Ticket</h2>
          
          <div className="event-info">
            <h3>{event.name}</h3>
            <p className="event-description">{event.description}</p>
            
            <div className="event-meta">
              <div className="meta-item">
                <i className="fas fa-clock"></i>
                <span>{formatDate(event.date)}</span>
              </div>
              <div className="meta-item">
                <i className="fas fa-map-marker-alt"></i>
                <span>{event.location}</span>
              </div>
              <div className="meta-item">
                <i className="fas fa-ticket-alt"></i>
                <span>{event.available_tickets} tickets available</span>
              </div>
              <div className="meta-item price">
                <i className="fas fa-money-bill-wave"></i>
                <span>{formatPrice(event.ticket_price)}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="payment-form">
          <h3>Payment Details</h3>
          
          {error && (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          )}
          
          {success && (
            <div className="alert alert-success" role="alert">
              {success}
            </div>
          )}

          <form onSubmit={handlePurchase}>
            <div className="form-group">
              <label htmlFor="phoneNumber">M-Pesa Phone Number</label>
              <div className="input-group">
                <span className="input-group-text">+254</span>
                <input
                  type="text"
                  className="form-control"
                  id="phoneNumber"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  placeholder="712345678"
                  required
                  maxLength="9"
                />
              </div>
              <small className="form-text text-muted">
                Enter your M-Pesa registered phone number (without the 254 prefix)
              </small>
            </div>

            <div className="payment-summary">
              <h4>Payment Summary</h4>
              <div className="summary-item">
                <span>Ticket Price:</span>
                <span>{formatPrice(event.ticket_price)}</span>
              </div>
              <div className="summary-item total">
                <span>Total Amount:</span>
                <span>{formatPrice(event.ticket_price)}</span>
              </div>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary btn-lg w-100"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Processing...
                </>
              ) : (
                <>
                  <i className="fas fa-mobile-alt me-2"></i>
                  Pay with M-Pesa
                </>
              )}
            </button>
          </form>

          <div className="payment-info">
            <h5>Payment Instructions</h5>
            <ol>
              <li>Enter your M-Pesa registered phone number</li>
              <li>Click "Pay with M-Pesa"</li>
              <li>Check your phone for the M-Pesa STK Push notification</li>
              <li>Enter your M-Pesa PIN to complete the payment</li>
              <li>You'll receive a confirmation email with your ticket</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TicketPurchase;