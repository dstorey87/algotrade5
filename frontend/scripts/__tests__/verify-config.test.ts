/**
 * Test Suite for Configuration Verification
 * 
 * Tests configuration validation including:
 * - Required variables
 * - Value formats
 * - Environment-specific rules
 * - Error handling
 */

import { logger } from '../../src/utils/logger';

// Store original environment
const originalEnv = process.env;

// Mock logger
jest.mock('../../src/utils/logger', () => ({
  logger: {
    info: jest.fn(),
    error: jest.fn(),
  }
}));

describe('Configuration Verification', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset environment before each test
    process.env = { ...originalEnv };
    jest.resetModules();
  });

  afterAll(() => {
    // Restore original environment
    process.env = originalEnv;
  });

  describe('Development Environment', () => {
    beforeEach(() => {
      process.env.NODE_ENV = 'development';
    });

    it('should allow ws:// WebSocket URLs in development', () => {
      process.env.NEXT_PUBLIC_WS_URL = 'ws://localhost:8080';
      process.env.NEXT_PUBLIC_API_BASE_URL = 'http://localhost:3000';
      setValidConfig();
      
      // Should not throw error
      expect(() => require('../verify-config')).not.toThrow();
    });

    it('should allow debug mode in development', () => {
      process.env.NEXT_PUBLIC_DEBUG_MODE = 'true';
      setValidConfig();
      
      expect(() => require('../verify-config')).not.toThrow();
    });

    it('should warn but not throw on validation errors', () => {
      process.env.NEXT_PUBLIC_WS_RECONNECT_INTERVAL = 'invalid';
      setValidConfig();
      
      expect(() => require('../verify-config')).not.toThrow();
      expect(logger.error).toHaveBeenCalled();
    });
  });

  describe('Production Environment', () => {
    beforeEach(() => {
      process.env.NODE_ENV = 'production';
    });

    it('should require wss:// WebSocket URLs in production', () => {
      process.env.NEXT_PUBLIC_WS_URL = 'ws://api.example.com';
      setValidConfig();
      
      expect(() => require('../verify-config')).toThrow();
    });

    it('should require https:// API URLs in production', () => {
      process.env.NEXT_PUBLIC_API_BASE_URL = 'http://api.example.com';
      setValidConfig();
      
      expect(() => require('../verify-config')).toThrow();
    });

    it('should not allow debug mode in production', () => {
      process.env.NEXT_PUBLIC_DEBUG_MODE = 'true';
      setValidConfig();
      
      expect(() => require('../verify-config')).toThrow();
    });
  });

  describe('Required Variables', () => {
    it('should detect missing required variables', () => {
      // Only set some required variables
      process.env.NEXT_PUBLIC_WS_URL = 'wss://api.example.com';
      
      expect(() => require('../verify-config')).toThrow();
      expect(logger.error).toHaveBeenCalled();
    });

    it('should pass with all required variables set correctly', () => {
      setValidConfig();
      
      expect(() => require('../verify-config')).not.toThrow();
      expect(logger.info).toHaveBeenCalledWith(
        'Configuration validation successful',
        expect.any(Object)
      );
    });
  });

  describe('Value Validation', () => {
    beforeEach(() => {
      setValidConfig();
    });

    it('should validate WebSocket URL format', () => {
      process.env.NEXT_PUBLIC_WS_URL = 'invalid-url';
      expect(() => require('../verify-config')).toThrow();
    });

    it('should validate numeric ranges', () => {
      process.env.NEXT_PUBLIC_WS_RECONNECT_INTERVAL = '0';
      expect(() => require('../verify-config')).toThrow();

      process.env.NEXT_PUBLIC_WS_RECONNECT_INTERVAL = '70000';
      expect(() => require('../verify-config')).toThrow();
    });

    it('should validate boolean values', () => {
      process.env.NEXT_PUBLIC_TRADING_ENABLED = 'invalid';
      expect(() => require('../verify-config')).toThrow();
    });

    it('should validate log levels', () => {
      process.env.NEXT_PUBLIC_LOG_LEVEL = 'invalid';
      expect(() => require('../verify-config')).toThrow();

      process.env.NEXT_PUBLIC_LOG_LEVEL = 'debug';
      expect(() => require('../verify-config')).not.toThrow();
    });
  });
});

/**
 * Helper to set valid configuration values
 */
function setValidConfig() {
  process.env.NEXT_PUBLIC_WS_URL = 'wss://api.example.com';
  process.env.NEXT_PUBLIC_WS_RECONNECT_INTERVAL = '3000';
  process.env.NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS = '3';
  process.env.NEXT_PUBLIC_API_BASE_URL = 'https://api.example.com';
  process.env.NEXT_PUBLIC_API_TIMEOUT_MS = '15000';
  process.env.NEXT_PUBLIC_INITIAL_INVESTMENT = '10';
  process.env.NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT = '10';
  process.env.NEXT_PUBLIC_TRADING_ENABLED = 'false';
  process.env.NEXT_PUBLIC_ENABLE_PAPER_TRADING = 'true';
  process.env.NEXT_PUBLIC_ENABLE_LIVE_TRADING = 'false';
  process.env.NEXT_PUBLIC_ENABLE_QUANTUM_BACKTESTING = 'true';
  process.env.NEXT_PUBLIC_LOG_LEVEL = 'warn';
  process.env.NEXT_PUBLIC_DEBUG_MODE = 'false';
}