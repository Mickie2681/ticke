import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { Link } from 'react-router-dom';

const EventDetail = () => {
  const { id } = useParams();
  const [event, setEvent] = useState(null);

  useEffect(() => {
    api.get(`/events/${id}/`).then(response => setEvent(response.data));
  }, [id]);

  return (
    <div>
      {event ? (
        <>
          <h1>{event.name}</h1>
          <p>{event.description}</p>
          <p>Date: {event.date}</p>
          <p>Location: {event.location}</p>
          <p>Price: ${event.ticket_price}</p>
          <p>Available: {event.available_tickets}</p>
          <Link to={`/purchase/${event.id}`}>Buy Ticket</Link>
        </>
      ) : <p>Loading...</p>}
    </div>
  );
};

export default EventDetail;