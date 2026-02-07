import api from './api';

export const adminEventService = {
  // Get all events (admin view)
  getAllEvents: () => api.get('/events/admin/'),
  
  // Create a new event
  createEvent: (eventData) => api.post('/events/admin/create/', eventData),
  
  // Update an existing event
  updateEvent: (eventId, eventData) => api.put(`/events/admin/${eventId}/update/`, eventData),
  
  // Delete an event
  deleteEvent: (eventId) => api.delete(`/events/admin/${eventId}/delete/`),
  
  // Get a single event
  getEvent: (eventId) => api.get(`/events/${eventId}/`),
};

