import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ApiTest = () => {
  const [backendStatus, setBackendStatus] = useState('unknown');
  const [apiResponse, setApiResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  // Test backend connection
  const testBackend = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Test health endpoint
      const healthResponse = await axios.get('http://localhost:8000/health/');
      console.log('Health check response:', healthResponse.data);
      
      // Test API endpoint
      const apiResponse = await axios.get('http://localhost:8000/api/test/');
      console.log('API test response:', apiResponse.data);
      
      setBackendStatus('connected');
      setApiResponse({
        health: healthResponse.data,
        api: apiResponse.data
      });
    } catch (err) {
      console.error('Backend connection error:', err);
      setBackendStatus('error');
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Test events API
  const testEventsApi = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get('http://localhost:8000/api/events/');
      console.log('Events API response:', response.data);
      setApiResponse(prev => ({ ...prev, events: response.data }));
    } catch (err) {
      console.error('Events API error:', err);
      setError(`Events API error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Auto-test on component mount
    testBackend();
  }, []);

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2>🔌 API Connection Test</h2>
      <p>Testing connection to Django backend at <code>http://localhost:8000</code></p>
      
      <div style={{ marginBottom: '20px' }}>
        <button 
          onClick={testBackend}
          disabled={loading}
          style={{
            padding: '10px 20px',
            marginRight: '10px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Testing...' : 'Test Backend Connection'}
        </button>
        
        <button 
          onClick={testEventsApi}
          disabled={loading || backendStatus !== 'connected'}
          style={{
            padding: '10px 20px',
            backgroundColor: backendStatus === 'connected' ? '#28a745' : '#6c757d',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: (loading || backendStatus !== 'connected') ? 'not-allowed' : 'pointer'
          }}
        >
          Test Events API
        </button>
      </div>

      {/* Status Display */}
      <div style={{ 
        padding: '15px', 
        borderRadius: '5px', 
        marginBottom: '20px',
        backgroundColor: backendStatus === 'connected' ? '#d4edda' : 
                       backendStatus === 'error' ? '#f8d7da' : '#fff3cd',
        border: `1px solid ${
          backendStatus === 'connected' ? '#c3e6cb' : 
          backendStatus === 'error' ? '#f5c6cb' : '#ffeaa7'
        }`
      }}>
        <strong>Backend Status: </strong>
        <span style={{ 
          color: backendStatus === 'connected' ? '#155724' : 
                 backendStatus === 'error' ? '#721c24' : '#856404'
        }}>
          {backendStatus === 'connected' ? '✅ Connected' : 
           backendStatus === 'error' ? '❌ Connection Failed' : '⏳ Testing...'}
        </span>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{ 
          padding: '15px', 
          backgroundColor: '#f8d7da', 
          border: '1px solid #f5c6cb', 
          borderRadius: '5px', 
          marginBottom: '20px',
          color: '#721c24'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Response Display */}
      {apiResponse && (
        <div style={{ 
          padding: '15px', 
          backgroundColor: '#f8f9fa', 
          border: '1px solid #dee2e6', 
          borderRadius: '5px'
        }}>
          <h3>📊 API Responses:</h3>
          
          {apiResponse.health && (
            <div style={{ marginBottom: '15px' }}>
              <h4>Health Check:</h4>
              <pre style={{ 
                backgroundColor: '#e9ecef', 
                padding: '10px', 
                borderRadius: '3px',
                overflow: 'auto'
              }}>
                {JSON.stringify(apiResponse.health, null, 2)}
              </pre>
            </div>
          )}
          
          {apiResponse.api && (
            <div style={{ marginBottom: '15px' }}>
              <h4>API Test:</h4>
              <pre style={{ 
                backgroundColor: '#e9ecef', 
                padding: '10px', 
                borderRadius: '3px',
                overflow: 'auto'
              }}>
                {JSON.stringify(apiResponse.api, null, 2)}
              </pre>
            </div>
          )}
          
          {apiResponse.events && (
            <div>
              <h4>Events API:</h4>
              <pre style={{ 
                backgroundColor: '#e9ecef', 
                padding: '10px', 
                borderRadius: '3px',
                overflow: 'auto'
              }}>
                {JSON.stringify(apiResponse.events, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}

      {/* Troubleshooting Tips */}
      <div style={{ 
        marginTop: '30px', 
        padding: '20px', 
        backgroundColor: '#e7f3ff', 
        border: '1px solid #b3d9ff', 
        borderRadius: '5px'
      }}>
        <h3>🔧 Troubleshooting Tips:</h3>
        <ul>
          <li><strong>Backend not running:</strong> Make sure Django is running on port 8000</li>
          <li><strong>CORS issues:</strong> Check Django CORS settings</li>
          <li><strong>Port conflicts:</strong> Ensure no other service is using port 8000</li>
          <li><strong>Firewall:</strong> Check if firewall is blocking connections</li>
          <li><strong>Network:</strong> Verify you can access localhost:8000 in browser</li>
        </ul>
      </div>
    </div>
  );
};

export default ApiTest;












