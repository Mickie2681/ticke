import React, { useState, useEffect } from 'react';
import { Navigate } from 'react-router-dom';
import './AdminProtected.css';

const AdminProtected = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const userInfo = localStorage.getItem('userInfo');
    if (userInfo) {
      try {
        setUser(JSON.parse(userInfo));
      } catch (error) {
        console.error('Error parsing user info:', error);
      }
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="admin-loading">Checking permissions...</div>;
  }

  const isAdmin = user?.is_staff || user?.is_superuser;
  const isAuthenticated = !!localStorage.getItem('accessToken');

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!isAdmin) {
    return (
      <div className="admin-access-denied">
        <h2>Access Denied</h2>
        <p>You don't have permission to access this area. Admin privileges required.</p>
      </div>
    );
  }

  return children;
};

export default AdminProtected;
