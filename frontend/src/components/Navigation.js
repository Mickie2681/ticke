import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState(null);
  const isAuthenticated = !!localStorage.getItem('accessToken');

  useEffect(() => {
    // Get user info from localStorage if available
    const userInfo = localStorage.getItem('userInfo');
    if (userInfo) {
      try {
        setUser(JSON.parse(userInfo));
      } catch (error) {
        console.error('Error parsing user info:', error);
      }
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userInfo');
    setUser(null);
    navigate('/login');
  };

  const isAdmin = user?.is_staff || user?.is_superuser;

  // Function to check if a link is active
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
      <div className="container">
        <Link className="navbar-brand" to="/">Ticket System</Link>
        
        <div className="navbar-nav ms-auto">
          {isAuthenticated ? (
            <>
              <Link 
                className={`nav-link ${isActive('/') ? 'active' : ''}`} 
                to="/"
              >
                Events
              </Link>
              <Link 
                className={`nav-link ${isActive('/purchase') ? 'active' : ''}`} 
                to="/purchase"
              >
                Purchase
              </Link>
              <Link 
                className={`nav-link ${isActive('/my-tickets') ? 'active' : ''}`} 
                to="/my-tickets"
              >
                My Tickets
              </Link>
              {isAdmin && (
                <Link 
                  className={`nav-link ${isActive('/admin/events') ? 'active' : ''}`} 
                  to="/admin/events"
                >
                  Admin Events
                </Link>
              )}
              <button 
                className="btn btn-outline-light ms-2" 
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link className="nav-link" to="/login">Login</Link>
              <Link className="nav-link" to="/register">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
