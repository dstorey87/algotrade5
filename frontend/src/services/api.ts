import axios from 'axios';

// Create main FreqTrade API instance
const freqtradeApi = axios.create({
  baseURL: import.meta.env.VITE_FREQTRADE_API_URL || 'http://localhost:8080',
  timeout: 10000,
  auth: {
    username: 'freqtrade',
    password: 'freqtrade'
  }
});

// Create AlgoTradePro5 API instance
const algoTradeApi = axios.create({
  baseURL: import.meta.env.VITE_ALGOTRADE_API_URL || 'http://localhost:8000',
  timeout: 15000
});

// Add response interceptors for error handling
const addErrorInterceptor = (apiInstance) => {
  apiInstance.interceptors.response.use(
    response => response,
    error => {
      console.error('API Error:', error);
      return Promise.reject(error);
    }
  );
};

addErrorInterceptor(freqtradeApi);
addErrorInterceptor(algoTradeApi);

// FreqTrade standard API endpoints
export const freqtradeService = {
  // System status
  getStatus: () => freqtradeApi.get('/status'),
  getVersion: () => freqtradeApi.get('/version'),
  
  // Trading data
  getBalance: () => freqtradeApi.get('/balance'),
  getTrades: (limit?: number) => freqtradeApi.get('/trades', { params: { limit } }),
  getDailyStats: () => freqtradeApi.get('/daily'),
  getPerformance: () => freqtradeApi.get('/performance'),
  
  // Strategy management
  getStrategyList: () => freqtradeApi.get('/strategies'),
  getCurrentStrategy: () => freqtradeApi.get('/strategy'),
  updateStrategy: (params: any) => freqtradeApi.post('/strategy', params),
  
  // Trading controls
  startTrading: () => freqtradeApi.post('/start'),
  stopTrading: () => freqtradeApi.post('/stop'),
  emergencyStop: () => freqtradeApi.post('/stopbuy'),
  
  // Trade actions
  forceBuy: (payload: any) => freqtradeApi.post('/forcebuy', payload),
  forceSell: (payload: any) => freqtradeApi.post('/forcesell', payload),
  
  // System management
  reloadConfig: () => freqtradeApi.post('/reload_config'),
  getLogs: () => freqtradeApi.get('/logs')
};

// AlgoTradePro5 custom API endpoints
export const systemService = {
  // System metrics and logs
  getSystemMetrics: () => algoTradeApi.get('/api/v1/system/metrics'),
  getSystemLogs: () => algoTradeApi.get('/api/v1/system/logs')
};

// Health monitoring API
export const healthService = {
  // System health
  getHealthStatus: () => algoTradeApi.get('/api/v1/health/status'),
  getComponentHealth: (componentType?: string) => 
    algoTradeApi.get('/api/v1/health/components', { params: { component_type: componentType } }),
  runDiagnostics: () => algoTradeApi.get('/api/v1/health/diagnostics'),
  
  // Resource monitoring
  getResourceUtilization: () => algoTradeApi.get('/api/v1/health/resources'),
  getGpuStatus: () => algoTradeApi.get('/api/v1/health/gpu'),
  getDatabaseHealth: () => algoTradeApi.get('/api/v1/health/database'),
  
  // Component-specific checks
  checkComponentHealth: (componentId: string) => 
    algoTradeApi.post(`/api/v1/health/check/${componentId}`)
};

// Machine Learning API
export const mlService = {
  // Model management
  getAvailableModels: () => algoTradeApi.get('/api/v1/ml/models'),
  getModelStatus: (modelId: string) => algoTradeApi.get(`/api/v1/ml/models/${modelId}/status`),
  loadModel: (modelId: string) => algoTradeApi.post(`/api/v1/ml/models/${modelId}/load`),
  unloadModel: (modelId: string) => algoTradeApi.post(`/api/v1/ml/models/${modelId}/unload`),
  
  // Predictions
  runPrediction: (modelId: string, data: any) => 
    algoTradeApi.post(`/api/v1/ml/models/${modelId}/predict`, data),
  
  // Performance metrics
  getPerformanceMetrics: () => algoTradeApi.get('/api/v1/ml/performance')
};

// AI components API
export const aiService = {
  // LLM operations
  getAvailableLlmModels: () => algoTradeApi.get('/api/v1/ai/llm/models'),
  generateLlmResponse: (modelId: string, prompt: any) => 
    algoTradeApi.post('/api/v1/ai/llm/generate', { model_id: modelId, ...prompt }),
  
  // Quantum operations
  getQuantumStatus: () => algoTradeApi.get('/api/v1/ai/quantum/status'),
  executeQuantumCircuit: (circuitData: any) => 
    algoTradeApi.post('/api/v1/ai/quantum/execute', circuitData),
  getQuantumJobStatus: (taskId: string) => 
    algoTradeApi.get(`/api/v1/ai/quantum/jobs/${taskId}`),
  
  // Strategy analysis
  analyzeStrategy: (strategyId: string, timeframe: string = '1d', pair: string = 'BTC/USDT') => 
    algoTradeApi.get('/api/v1/ai/strategies/analyze', { 
      params: { strategy_id: strategyId, timeframe, pair } 
    })
};

// Trading control API
export const tradingService = {
  // Trading status
  getTradingStatus: () => algoTradeApi.get('/api/v1/trading/status'),
  
  // Trading controls
  startTrading: (strategyId?: string) => 
    algoTradeApi.post('/api/v1/trading/start', { strategy_id: strategyId }),
  stopTrading: (emergency: boolean = false) => 
    algoTradeApi.post('/api/v1/trading/stop', { emergency }),
  
  // Strategy management
  getAvailableStrategies: () => algoTradeApi.get('/api/v1/trading/strategies'),
  getStrategyDetails: (strategyId: string) => 
    algoTradeApi.get(`/api/v1/trading/strategies/${strategyId}`),
  activateStrategy: (strategyId: string) => 
    algoTradeApi.post(`/api/v1/trading/strategies/${strategyId}/activate`),
  
  // Performance metrics
  getTradingPerformance: (timeframe: string = '1d') => 
    algoTradeApi.get('/api/v1/trading/performance', { params: { timeframe } }),
  
  // Risk management
  getRiskMetrics: () => algoTradeApi.get('/api/v1/trading/risk'),
  updateRiskParameters: (parameters: any) => 
    algoTradeApi.post('/api/v1/trading/risk/update', parameters),
  
  // Manual trading
  executeManualTrade: (tradeData: any) => 
    algoTradeApi.post('/api/v1/trading/execute_trade', tradeData)
};

// Combined API for backward compatibility
export const tradingApi = {
  ...freqtradeService,
  ...systemService,
  getSystemMetrics: systemService.getSystemMetrics,
  getSystemLogs: systemService.getSystemLogs
};

export default {
  freqtrade: freqtradeApi,
  algoTrade: algoTradeApi,
  services: {
    freqtradeService,
    systemService,
    healthService,
    mlService,
    aiService,
    tradingService
  }
};