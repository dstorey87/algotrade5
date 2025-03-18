// API and WebSocket connection settings
const env = process.env.NODE_ENV || 'development';

// Default settings by environment
const config = {
  development: {
    // Local development settings
    apiBaseUrl: 'http://localhost:8080',
    wsBaseUrl: 'ws://localhost:8080',
    apiVersion: 'v1',
    pollingInterval: 5000,
    tokenStorageKey: 'api_token',
  },
  production: {
    // Production settings
    apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || 'https://api.algotradepro5.com',
    wsBaseUrl: process.env.NEXT_PUBLIC_WS_BASE_URL || 'wss://api.algotradepro5.com',
    apiVersion: 'v1',
    pollingInterval: 10000,
    tokenStorageKey: 'api_token',
  },
  test: {
    // Test environment settings
    apiBaseUrl: 'http://localhost:8080',
    wsBaseUrl: 'ws://localhost:8080',
    apiVersion: 'v1',
    pollingInterval: 1000,
    tokenStorageKey: 'test_api_token',
  }
};

// Override with environment variables if present
const apiConfig = {
  ...config[env as keyof typeof config],
  apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL || config[env as keyof typeof config].apiBaseUrl,
  wsBaseUrl: process.env.NEXT_PUBLIC_WS_BASE_URL || config[env as keyof typeof config].wsBaseUrl,
};

// Helper functions for working with API endpoints
const apiSettings = {
  ...apiConfig,
  
  // Build API URL with path
  apiUrl: (path: string): string => {
    return `${apiConfig.apiBaseUrl}/api/${apiConfig.apiVersion}/${path.replace(/^\//, '')}`;
  },
  
  // Build WebSocket URL with path
  wsUrl: (path: string): string => {
    return `${apiConfig.wsBaseUrl}/api/${apiConfig.apiVersion}/ws/${path.replace(/^\//, '')}`;
  },
  
  // Get auth token from storage
  getToken: (): string => {
    if (typeof window === 'undefined') return '';
    return localStorage.getItem(apiConfig.tokenStorageKey) || '';
  },
  
  // Set auth token in storage
  setToken: (token: string): void => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(apiConfig.tokenStorageKey, token);
  },
  
  // Clear auth token from storage
  clearToken: (): void => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(apiConfig.tokenStorageKey);
  }
};

export default apiSettings;