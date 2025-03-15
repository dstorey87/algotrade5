import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_FREQTRADE_API_URL,
  timeout: 10000,
  auth: {
    username: 'freqtrade',
    password: 'freqtrade'
  }
});

export const tradingApi = {
  getSystemStatus: () => api.get('/status'),
  getBalance: () => api.get('/balance'),
  getTrades: () => api.get('/trades'),
  getDailyStats: () => api.get('/daily'),
  getPerformance: () => api.get('/performance'),
  getStrategyList: () => api.get('/strategies'),
  
  // Trading controls
  startTrading: () => api.post('/start'),
  stopTrading: () => api.post('/stop'),
  emergencyStop: () => api.post('/stopbuy'),
  
  // Strategy management
  getCurrentStrategy: () => api.get('/strategy'),
  updateStrategy: (params: any) => api.post('/strategy', params),
  
  // Trade actions
  forceBuy: (payload: any) => api.post('/forcebuy', payload),
  forceSell: (payload: any) => api.post('/forcesell', payload),

  // System management
  reloadConfig: () => api.post('/reload_config'),
  getLogs: () => api.get('/logs'),
};

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;