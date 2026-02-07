import React, { useState, useEffect } from 'react';
import { adminEventService } from '../services/adminApi';
import './AdminEventManager.css';

const AdminEventManager = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingEvent, setEditingEvent] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    date: '',
    location: '',
    ticket_price: '',
    available_tickets: ''
  });

  useEffect(() => {
    loadEvents();
  }, []);

  const loadEvents = async () => {
    setLoading(true);
    try {
      const response = await adminEventService.getAllEvents();
      setEvents(response.data);
      setError('');
    } catch (err) {
      setError('Failed to load events. Please check your admin permissions.');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      date: '',
      location: '',
      ticket_price: '',
      available_tickets: ''
    });
    setEditingEvent(null);
    setShowForm(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const eventData = {
        ...formData,
        ticket_price: parseFloat(formData.ticket_price),
        available_tickets: parseInt(formData.available_tickets)
      };

      if (editingEvent) {
        await adminEventService.updateEvent(editingEvent.id, eventData);
      } else {
        await adminEventService.createEvent(eventData);
      }

      await loadEvents();
      resetForm();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to save event');
      console.error('Error saving event:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (event) => {
    setEditingEvent(event);
    setFormData({
      name: event.name,
      description: event.description,
      date: event.date.slice(0, 16), // Format for datetime-local input
      location: event.location,
      ticket_price: event.ticket_price.toString(),
      available_tickets: event.available_tickets.toString()
    });
    setShowForm(true);
  };

  const handleDelete = async (eventId) => {
    if (!window.confirm('Are you sure you want to delete this event?')) {
      return;
    }

    setLoading(true);
    try {
      await adminEventService.deleteEvent(eventId);
      await loadEvents();
      setError('');
    } catch (err) {
      setError('Failed to delete event');
      console.error('Error deleting event:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  if (loading && events.length === 0) {
    return <div className="admin-loading">Loading events...</div>;
  }

  return (
    <div className="admin-event-manager">
      <div className="admin-header">
        <h2>Event Management</h2>
        <button 
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Add New Event'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <div className="event-form-container">
          <h3>{editingEvent ? 'Edit Event' : 'Create New Event'}</h3>
          <form onSubmit={handleSubmit} className="event-form">
            <div className="form-group">
              <label htmlFor="name">Event Name *</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                required
                className="form-control"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description *</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                required
                className="form-control"
                rows="4"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="date">Date & Time *</label>
                <input
                  type="datetime-local"
                  id="date"
                  name="date"
                  value={formData.date}
                  onChange={handleInputChange}
                  required
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label htmlFor="location">Location *</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  required
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="ticket_price">Ticket Price ($) *</label>
                <input
                  type="number"
                  id="ticket_price"
                  name="ticket_price"
                  value={formData.ticket_price}
                  onChange={handleInputChange}
                  required
                  min="0"
                  step="0.01"
                  className="form-control"
                />
              </div>

              <div className="form-group">
                <label htmlFor="available_tickets">Available Tickets *</label>
                <input
                  type="number"
                  id="available_tickets"
                  name="available_tickets"
                  value={formData.available_tickets}
                  onChange={handleInputChange}
                  required
                  min="1"
                  className="form-control"
                />
              </div>
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="btn btn-success"
                disabled={loading}
              >
                {loading ? 'Saving...' : (editingEvent ? 'Update Event' : 'Create Event')}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={resetForm}
                disabled={loading}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="events-list">
        <h3>All Events ({events.length})</h3>
        {events.length === 0 ? (
          <p className="no-events">No events found. Create your first event!</p>
        ) : (
          <div className="events-grid">
            {events.map(event => (
              <div key={event.id} className="event-card">
                <div className="event-header">
                  <h4>{event.name}</h4>
                  <div className="event-actions">
                    <button 
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => handleEdit(event)}
                    >
                      Edit
                    </button>
                    <button 
                      className="btn btn-sm btn-outline-danger"
                      onClick={() => handleDelete(event.id)}
                    >
                      Delete
                    </button>
                  </div>
                </div>
                <p className="event-description">{event.description}</p>
                <div className="event-details">
                  <div className="detail-item">
                    <strong>Date:</strong> {formatDate(event.date)}
                  </div>
                  <div className="detail-item">
                    <strong>Location:</strong> {event.location}
                  </div>
                  <div className="detail-item">
                    <strong>Price:</strong> ${event.ticket_price}
                  </div>
                  <div className="detail-item">
                    <strong>Available:</strong> {event.available_tickets} tickets
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminEventManager;

