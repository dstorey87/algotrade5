import axios from 'axios';

const BASE_URL = process.env.NEXT_PUBLIC_FREQTRADE_API_URL || 'http://localhost:8080/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
});

export interface SystemStatus {
  status: string;
  version: string;
  strategy: string | null;
  running: boolean;
}

export interface Balance {
  total: number;
  free: number;
  used: number;
  stake: string;
}

export const freqtradeApi = {
  getStatus: () => api.get<SystemStatus>('/status'),
  getBalance: () => api.get<Balance>('/balance'),
  startBot: () => api.post('/start'),
  stopBot: () => api.post('/stop'),
  getStrategies: () => api.get('/strategies'),
  getPerformance: () => api.get('/performance'),
  getDailyStats: () => api.get('/daily'),
  getProfit: () => api.get('/profit'),
  getOpenTrades: () => api.get('/status'),
  forceSell: (tradeId: number) => api.post(`/forcesell/${tradeId}`),
  forceBuy: (pair: string) => api.post('/forcebuy', { pair }),
  reloadConfig: () => api.post('/reload_config'),
};