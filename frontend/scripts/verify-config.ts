/**
 * Configuration Verification Script
 * 
 * Validates environment variables during build process.
 * Runs as a pre-build step to ensure all required configuration is present.
 */

import { logger } from '../src/utils/logger';

interface ConfigValidation {
  required: boolean;
  validate?: (value: string) => boolean;
  errorMessage?: string;
}

/**
 * Configuration validation rules
 */
const CONFIG_RULES: Record<string, ConfigValidation> = {
  NEXT_PUBLIC_WS_URL: {
    required: true,
    validate: (value) => /^wss?:\/\/.+/.test(value),
    errorMessage: 'WebSocket URL must be a valid ws:// or wss:// URL'
  },
  NEXT_PUBLIC_WS_RECONNECT_INTERVAL: {
    required: true,
    validate: (value) => {
      const num = Number(value);
      return !isNaN(num) && num >= 1000 && num <= 60000;
    },
    errorMessage: 'WebSocket reconnect interval must be between 1000 and 60000 ms'
  },
  NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS: {
    required: true,
    validate: (value) => {
      const num = Number(value);
      return !isNaN(num) && num >= 1 && num <= 10;
    },
    errorMessage: 'Max reconnect attempts must be between 1 and 10'
  },
  NEXT_PUBLIC_API_BASE_URL: {
    required: true,
    validate: (value) => /^https?:\/\/.+/.test(value),
    errorMessage: 'API base URL must be a valid http:// or https:// URL'
  },
  NEXT_PUBLIC_API_TIMEOUT_MS: {
    required: true,
    validate: (value) => {
      const num = Number(value);
      return !isNaN(num) && num >= 1000 && num <= 60000;
    },
    errorMessage: 'API timeout must be between 1000 and 60000 ms'
  },
  NEXT_PUBLIC_INITIAL_INVESTMENT: {
    required: true,
    validate: (value) => {
      const num = Number(value);
      return !isNaN(num) && num >= 10 && num <= 1000;
    },
    errorMessage: 'Initial investment must be between 10 and 1000'
  },
  NEXT_PUBLIC_MAX_DRAWDOWN_PERCENT: {
    required: true,
    validate: (value) => {
      const num = Number(value);
      return !isNaN(num) && num > 0 && num <= 100;
    },
    errorMessage: 'Max drawdown percentage must be between 0 and 100'
  },
  NEXT_PUBLIC_TRADING_ENABLED: {
    required: true,
    validate: (value) => ['true', 'false'].includes(value.toLowerCase()),
    errorMessage: 'Trading enabled must be true or false'
  },
  NEXT_PUBLIC_ENABLE_PAPER_TRADING: {
    required: true,
    validate: (value) => ['true', 'false'].includes(value.toLowerCase()),
    errorMessage: 'Paper trading enabled must be true or false'
  },
  NEXT_PUBLIC_ENABLE_LIVE_TRADING: {
    required: true,
    validate: (value) => ['true', 'false'].includes(value.toLowerCase()),
    errorMessage: 'Live trading enabled must be true or false'
  },
  NEXT_PUBLIC_ENABLE_QUANTUM_BACKTESTING: {
    required: true,
    validate: (value) => ['true', 'false'].includes(value.toLowerCase()),
    errorMessage: 'Quantum backtesting enabled must be true or false'
  },
  NEXT_PUBLIC_LOG_LEVEL: {
    required: true,
    validate: (value) => ['debug', 'info', 'warn', 'error'].includes(value.toLowerCase()),
    errorMessage: 'Log level must be one of: debug, info, warn, error'
  },
  NEXT_PUBLIC_DEBUG_MODE: {
    required: true,
    validate: (value) => ['true', 'false'].includes(value.toLowerCase()),
    errorMessage: 'Debug mode must be true or false'
  }
};

/**
 * Verify all configuration values
 */
function verifyConfig(): void {
  const errors: string[] = [];
  const environment = process.env.NODE_ENV || 'development';

  logger.info('Verifying configuration', {
    environment,
    timestamp: new Date().toISOString()
  });

  // Check each configuration rule
  Object.entries(CONFIG_RULES).forEach(([key, rule]) => {
    const value = process.env[key];

    // Check if required value is present
    if (rule.required && !value) {
      errors.push(`Missing required environment variable: ${key}`);
      return;
    }

    // Validate value format if validator exists
    if (value && rule.validate && !rule.validate(value)) {
      errors.push(rule.errorMessage || `Invalid value for ${key}: ${value}`);
    }
  });

  // Production-specific validations
  if (environment === 'production') {
    // Ensure secure WebSocket connection in production
    if (!process.env.NEXT_PUBLIC_WS_URL?.startsWith('wss://')) {
      errors.push('Production WebSocket URL must use wss:// protocol');
    }

    // Ensure secure API connection in production
    if (!process.env.NEXT_PUBLIC_API_BASE_URL?.startsWith('https://')) {
      errors.push('Production API URL must use https:// protocol');
    }

    // Ensure debug mode is disabled in production
    if (process.env.NEXT_PUBLIC_DEBUG_MODE === 'true') {
      errors.push('Debug mode must be disabled in production');
    }
  }

  // Log validation results
  if (errors.length > 0) {
    logger.error('Configuration validation failed', {
      errors,
      environment,
      timestamp: new Date().toISOString()
    });

    // Exit with error in production, just warn in development
    if (environment === 'production') {
      throw new Error('Configuration validation failed:\n' + errors.join('\n'));
    }
  } else {
    logger.info('Configuration validation successful', {
      environment,
      timestamp: new Date().toISOString()
    });
  }
}

// Run verification
verifyConfig();