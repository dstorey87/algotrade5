/**
 * Test Suite for Environment Configuration
 * 
 * Tests configuration loading and validation including:
 * - Environment variable loading
 * - Default values
 * - Validation rules
 * - Error handling
 */

import { config, getConfig } from '../config';
import { logger } from '../logger';

// Mock the logger
jest.mock('../logger', () => ({
  logger: {
    info: jest.fn(),
    error: jest.fn(),
  },
}));

describe('Environment Configuration', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.clearAllMocks();
    // Reset environment variables before each test
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    // Restore original environment
    process.env = originalEnv;
  });

  describe('Default Configuration', () => {
    it('should load default values when no environment variables are set', () => {
      expect(config).toEqual(expect.objectContaining({
        wsUrl: 'ws://localhost:8080',
        wsReconnectInterval: 5000,
        wsMaxReconnectAttempts: 5,
        initialInvestment: 10,
        maxDrawdownPercent: 10,
        tradingEnabled: false
      }));
    });

    it('should log successful configuration loading', () => {
      expect(logger.info).toHaveBeenCalledWith(
        'Configuration loaded successfully',
        expect.any(Object)
      );
    });
  });

  describe('Environment Variable Override', () => {
    beforeEach(() => {
      // Set test environment variables
      process.env.NEXT_PUBLIC_WS_URL = 'ws://test-server:8080';
      process.env.NEXT_PUBLIC_INITIAL_INVESTMENT = '20';
      process.env.NEXT_PUBLIC_TRADING_ENABLED = 'true';
    });

    it('should override default values with environment variables', () => {
      expect(config).toEqual(expect.objectContaining({
        wsUrl: 'ws://test-server:8080',
        initialInvestment: 20,
        tradingEnabled: true
      }));
    });
  });

  describe('Validation Rules', () => {
    it('should validate WebSocket URL format', () => {
      process.env.NEXT_PUBLIC_WS_URL = 'invalid-url';
      expect(() => require('../config')).toThrow();
    });

    it('should validate numeric ranges', () => {
      process.env.NEXT_PUBLIC_INITIAL_INVESTMENT = '5'; // Below minimum
      expect(() => require('../config')).toThrow();
    });

    it('should validate boolean values', () => {
      process.env.NEXT_PUBLIC_TRADING_ENABLED = 'invalid';
      expect(() => require('../config')).toThrow();
    });
  });

  describe('Production Environment', () => {
    const originalNodeEnv = process.env.NODE_ENV;

    beforeEach(() => {
      process.env.NODE_ENV = 'production';
    });

    afterAll(() => {
      process.env.NODE_ENV = originalNodeEnv;
    });

    it('should throw error in production when validation fails', () => {
      process.env.NEXT_PUBLIC_WS_URL = 'invalid-url';
      expect(() => require('../config')).toThrow();
    });
  });

  describe('Sensitive Information Handling', () => {
    it('should mask sensitive information in logs', () => {
      process.env.NEXT_PUBLIC_WS_URL = 'ws://user:pass@server:8080';
      
      require('../config');

      expect(logger.info).toHaveBeenCalledWith(
        'Configuration loaded successfully',
        expect.objectContaining({
          config: expect.objectContaining({
            wsUrl: expect.stringContaining('//***@')
          })
        })
      );
    });
  });

  describe('Feature Flags', () => {
    it('should properly handle feature flag configuration', () => {
      process.env.NEXT_PUBLIC_ENABLE_PAPER_TRADING = 'true';
      process.env.NEXT_PUBLIC_ENABLE_LIVE_TRADING = 'false';
      
      expect(config).toEqual(expect.objectContaining({
        enablePaperTrading: true,
        enableLiveTrading: false
      }));
    });
  });
});

describe('Configuration Parser', () => {
  const originalEnv = process.env;

  beforeEach(() => {
    jest.resetModules();
    process.env = {
      ...originalEnv,
      // Set up test environment variables
      NEXT_PUBLIC_WS_URL: 'ws://localhost:8080',
      NEXT_PUBLIC_WS_RECONNECT_INTERVAL: '5000',
      NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS: '5',
      NEXT_PUBLIC_API_BASE_URL: 'http://localhost:8000',
      NEXT_PUBLIC_API_TIMEOUT_MS: '30000',
      NEXT_PUBLIC_INITIAL_INVESTMENT: '10',
      NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT: '10',
      NEXT_PUBLIC_TRADING_ENABLED: 'false',
      NEXT_PUBLIC_ENABLE_PAPER_TRADING: 'true',
      NEXT_PUBLIC_ENABLE_LIVE_TRADING: 'false',
      NEXT_PUBLIC_ENABLE_QUANTUM_BACKTESTING: 'true',
      NEXT_PUBLIC_LOG_LEVEL: 'info',
      NEXT_PUBLIC_DEBUG_MODE: 'true',
    };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  it('should parse valid configuration correctly', () => {
    const config = getConfig();
    expect(config).toEqual({
      ws: {
        url: 'ws://localhost:8080',
        reconnectInterval: 5000,
        maxReconnectAttempts: 5,
      },
      api: {
        baseUrl: 'http://localhost:8000',
        timeoutMs: 30000,
      },
      trading: {
        initialInvestment: 10,
        maxDrawdownPercent: 10,
        enabled: false,
      },
      features: {
        paperTrading: true,
        liveTrading: false,
        quantumBacktesting: true,
      },
      system: {
        logLevel: 'info',
        debugMode: true,
      },
    });
  });

  it('should throw error for missing required values', () => {
    delete process.env.NEXT_PUBLIC_WS_URL;
    expect(() => getConfig()).toThrow('Missing required environment variable: NEXT_PUBLIC_WS_URL');
  });

  it('should throw error for invalid number values', () => {
    process.env.NEXT_PUBLIC_API_TIMEOUT_MS = 'invalid';
    expect(() => getConfig()).toThrow('Invalid value for NEXT_PUBLIC_API_TIMEOUT_MS');
  });

  it('should throw error for out of range values', () => {
    process.env.NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT = '101';
    expect(() => getConfig()).toThrow('Must be a number between 0 and 100');
  });

  it('should throw error for invalid boolean values', () => {
    process.env.NEXT_PUBLIC_TRADING_ENABLED = 'maybe';
    expect(() => getConfig()).toThrow("Must be 'true' or 'false'");
  });

  it('should throw error for invalid log levels', () => {
    process.env.NEXT_PUBLIC_LOG_LEVEL = 'invalid';
    expect(() => getConfig()).toThrow('Must be one of: debug, info, warn, error');
  });
});