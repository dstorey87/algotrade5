/**
 * Environment Configuration Utility
 * 
 * Centralizes environment configuration management with:
 * - Type-safe configuration access
 * - Validation of required values
 * - Default values for development
 * - Comprehensive logging of configuration issues
 */

import { logger } from './logger';

/**
 * Environment configuration interface
 */
interface EnvConfig {
  // WebSocket Configuration
  wsUrl: string;
  wsReconnectInterval: number;
  wsMaxReconnectAttempts: number;

  // API Configuration
  apiBaseUrl: string;
  apiTimeoutMs: number;

  // Trading Configuration
  initialInvestment: number;
  maxDrawdownPercent: number;
  tradingEnabled: boolean;

  // Feature Flags
  enablePaperTrading: boolean;
  enableLiveTrading: boolean;
  enableQuantumBacktesting: boolean;

  // System Configuration
  logLevel: string;
  debugMode: boolean;
}

/**
 * Default configuration values
 * Used in development and as fallbacks
 */
const defaultConfig: EnvConfig = {
  // WebSocket defaults
  wsUrl: 'ws://localhost:8080',
  wsReconnectInterval: 5000,
  wsMaxReconnectAttempts: 5,

  // API defaults
  apiBaseUrl: 'http://localhost:8000',
  apiTimeoutMs: 30000,

  // Trading defaults
  initialInvestment: 10,
  maxDrawdownPercent: 10,
  tradingEnabled: false,

  // Feature flag defaults
  enablePaperTrading: true,
  enableLiveTrading: false,
  enableQuantumBacktesting: true,

  // System defaults
  logLevel: 'info',
  debugMode: true
};

/**
 * Configuration validator type
 */
type ConfigValidator = {
  [K in keyof EnvConfig]: (value: any) => boolean;
};

/**
 * Validation rules for configuration values
 */
const configValidators: ConfigValidator = {
  wsUrl: (value: string) => /^wss?:\/\/.+/.test(value),
  wsReconnectInterval: (value: number) => value >= 1000 && value <= 60000,
  wsMaxReconnectAttempts: (value: number) => value >= 1 && value <= 10,
  
  apiBaseUrl: (value: string) => /^https?:\/\/.+/.test(value),
  apiTimeoutMs: (value: number) => value >= 1000 && value <= 60000,
  
  initialInvestment: (value: number) => value >= 10 && value <= 1000,
  maxDrawdownPercent: (value: number) => value > 0 && value <= 100,
  tradingEnabled: (value: boolean) => typeof value === 'boolean',
  
  enablePaperTrading: (value: boolean) => typeof value === 'boolean',
  enableLiveTrading: (value: boolean) => typeof value === 'boolean',
  enableQuantumBacktesting: (value: boolean) => typeof value === 'boolean',
  
  logLevel: (value: string) => ['debug', 'info', 'warn', 'error'].includes(value),
  debugMode: (value: boolean) => typeof value === 'boolean'
};

/**
 * Configuration parser for AlgoTradePro5 frontend
 * Validates and parses environment variables according to schema
 */

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface Config {
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
    logLevel: LogLevel;
    debugMode: boolean;
  };
}

const parseNumber = (value: string | undefined, varName: string): number => {
  if (!value) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
  const num = Number(value);
  if (isNaN(num)) {
    throw new Error(`Invalid value for ${varName}`);
  }
  return num;
};

const parseBoolean = (value: string | undefined, varName: string): boolean => {
  if (!value) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
  if (value !== 'true' && value !== 'false') {
    throw new Error(`Must be 'true' or 'false'`);
  }
  return value === 'true';
};

const parseLogLevel = (value: string | undefined): LogLevel => {
  if (!value) {
    throw new Error('Missing required environment variable: NEXT_PUBLIC_LOG_LEVEL');
  }
  if (!['debug', 'info', 'warn', 'error'].includes(value)) {
    throw new Error('Must be one of: debug, info, warn, error');
  }
  return value as LogLevel;
};

export const getConfig = (): Config => {
  // Validate required string values
  const wsUrl = process.env.NEXT_PUBLIC_WS_URL;
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (!wsUrl) throw new Error('Missing required environment variable: NEXT_PUBLIC_WS_URL');
  if (!apiBaseUrl) throw new Error('Missing required environment variable: NEXT_PUBLIC_API_BASE_URL');

  // Parse numeric values
  const reconnectInterval = parseNumber(process.env.NEXT_PUBLIC_WS_RECONNECT_INTERVAL, 'NEXT_PUBLIC_WS_RECONNECT_INTERVAL');
  const maxReconnectAttempts = parseNumber(process.env.NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS, 'NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS');
  const apiTimeoutMs = parseNumber(process.env.NEXT_PUBLIC_API_TIMEOUT_MS, 'NEXT_PUBLIC_API_TIMEOUT_MS');
  const initialInvestment = parseNumber(process.env.NEXT_PUBLIC_INITIAL_INVESTMENT, 'NEXT_PUBLIC_INITIAL_INVESTMENT');
  const maxDrawdownPercent = parseNumber(process.env.NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT, 'NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT');

  // Validate maxDrawdownPercent range
  if (maxDrawdownPercent < 0 || maxDrawdownPercent > 100) {
    throw new Error('Must be a number between 0 and 100');
  }

  // Parse boolean values
  const tradingEnabled = parseBoolean(process.env.NEXT_PUBLIC_TRADING_ENABLED, 'NEXT_PUBLIC_TRADING_ENABLED');
  const paperTrading = parseBoolean(process.env.NEXT_PUBLIC_ENABLE_PAPER_TRADING, 'NEXT_PUBLIC_ENABLE_PAPER_TRADING');
  const liveTrading = parseBoolean(process.env.NEXT_PUBLIC_ENABLE_LIVE_TRADING, 'NEXT_PUBLIC_ENABLE_LIVE_TRADING');
  const quantumBacktesting = parseBoolean(process.env.NEXT_PUBLIC_ENABLE_QUANTUM_BACKTESTING, 'NEXT_PUBLIC_ENABLE_QUANTUM_BACKTESTING');
  const debugMode = parseBoolean(process.env.NEXT_PUBLIC_DEBUG_MODE, 'NEXT_PUBLIC_DEBUG_MODE');

  // Parse log level
  const logLevel = parseLogLevel(process.env.NEXT_PUBLIC_LOG_LEVEL);

  return {
    ws: {
      url: wsUrl,
      reconnectInterval,
      maxReconnectAttempts,
    },
    api: {
      baseUrl: apiBaseUrl,
      timeoutMs: apiTimeoutMs,
    },
    trading: {
      initialInvestment,
      maxDrawdownPercent,
      enabled: tradingEnabled,
    },
    features: {
      paperTrading,
      liveTrading,
      quantumBacktesting,
    },
    system: {
      logLevel,
      debugMode,
    },
  };
};

// Export a singleton instance of the parsed config
export const config = getConfig();

/**
 * Re-export individual configuration values
 * This allows tree-shaking of unused values
 */
export const {
  wsUrl,
  wsReconnectInterval,
  wsMaxReconnectAttempts,
  apiBaseUrl,
  apiTimeoutMs,
  initialInvestment,
  maxDrawdownPercent,
  tradingEnabled,
  enablePaperTrading,
  enableLiveTrading,
  enableQuantumBacktesting,
  logLevel,
  debugMode
} = config;