import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // ✅ Your Django backend base
  // or use: baseURL: 'http://localhost:8000/api' 
});

export default api;
