import axios from 'axios';

// Automatically detect environment
const API_BASE_URL = import.meta.env.PROD 
  ? 'https://st-michael-app.onrender.com'
  : 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    
    // Debug logging (can remove in production)
    console.log('🔑 Token present:', !!token);
    console.log('🌐 API URL:', API_BASE_URL);
    
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.warn('⚠️ No token found in localStorage');
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.error('🚫 Unauthorized - redirecting to login');
      
      // Token expired or invalid - clear auth and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('auth');
      localStorage.removeItem('user');
      
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;