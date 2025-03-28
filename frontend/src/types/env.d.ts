/**
 * Environment Variable Type Definitions
 * 
 * Provides type safety and documentation for all environment variables
 * used in the AlgoTradePro5 frontend application.
 */

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      // WebSocket Configuration
      NEXT_PUBLIC_WS_URL: string;
      NEXT_PUBLIC_WS_RECONNECT_INTERVAL: string;
      NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS: string;

      // API Configuration
      NEXT_PUBLIC_API_BASE_URL: string;
      NEXT_PUBLIC_API_TIMEOUT_MS: string;

      // Trading Configuration
      NEXT_PUBLIC_INITIAL_INVESTMENT: string;
      NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT: string;
      NEXT_PUBLIC_TRADING_ENABLED: string;

      // Feature Flags
      NEXT_PUBLIC_ENABLE_PAPER_TRADING: string;
      NEXT_PUBLIC_ENABLE_LIVE_TRADING: string;
      NEXT_PUBLIC_ENABLE_QUANTUM_BACKTESTING: string;

      // System Configuration
      NEXT_PUBLIC_LOG_LEVEL: 'debug' | 'info' | 'warn' | 'error';
      NEXT_PUBLIC_DEBUG_MODE: string;

      // Node Environment
      NODE_ENV: 'development' | 'production' | 'test';
    }
  }
}

/**
 * Configuration value types after parsing
 */
export interface ParsedConfig {
  ws: {
    url: string;
    reconnectInterval: number;
    maxReconnectAttempts: number;
  };
  api: {
    baseUrl: string;
    timeoutMs: number;
  };
  trading: {
    initialInvestment: number;
    maxDrawdownPercent: number;
    enabled: boolean;
  };
  features: {
    paperTrading: boolean;
    liveTrading: boolean;
    quantumBacktesting: boolean;
  };
  system: {
    logLevel: 'debug' | 'info' | 'warn' | 'error';
    debugMode: boolean;
  };
}

// This export is necessary to make this a module
export {};