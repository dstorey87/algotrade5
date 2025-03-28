/**
 * Error logging utility for AlgoTradePro5 frontend
 * 
 * This module provides standardized error logging functionality:
 * - Structured error logs with timestamps and severity levels
 * - Console output for development
 * - Optional file logging for production
 * - Integration with monitoring systems
 */

// Severity levels for error categorization
export enum LogSeverity {
  DEBUG = 'debug',
  INFO = 'info',
  WARNING = 'warning',
  ERROR = 'error',
  CRITICAL = 'critical'
}

// Error categories to group related issues
export enum ErrorCategory {
  NETWORK = 'network',
  ROUTING = 'routing',
  API = 'api',
  WEBSOCKET = 'websocket',
  RENDERING = 'rendering',
  DATA = 'data',
  AUTHENTICATION = 'authentication'
}

// Logger interface for dependency injection and testing
export interface ILogger {
  debug(message: string, data?: any): void;
  info(message: string, data?: any): void;
  warn(message: string, data?: any): void;
  error(message: string, data?: any): void;
  critical(message: string, data?: any): void;
}

/**
 * Core logging service for application-wide error tracking
 */
class LoggerService implements ILogger {
  private isDevelopment = process.env.NODE_ENV !== 'production';
  
  /**
   * Format a log entry with consistent structure
   */
  private formatLogEntry(severity: LogSeverity, message: string, data?: any): string {
    const timestamp = new Date().toISOString();
    const logObject = {
      timestamp,
      severity,
      message,
      ...(data ? { data } : {})
    };
    
    return JSON.stringify(logObject);
  }
  
  /**
   * Write a debug-level message
   * @param message - The debug message
   * @param data - Optional data context
   */
  public debug(message: string, data?: any): void {
    if (this.isDevelopment) {
      console.debug(`[DEBUG] ${message}`, data || '');
    }
  }
  
  /**
   * Write an info-level message
   * @param message - The information message
   * @param data - Optional data context
   */
  public info(message: string, data?: any): void {
    console.info(`[INFO] ${message}`, data || '');
  }
  
  /**
   * Write a warning-level message
   * @param message - The warning message
   * @param data - Optional data context
   */
  public warn(message: string, data?: any): void {
    console.warn(`[WARNING] ${message}`, data || '');
    
    // In development, make warnings more visible
    if (this.isDevelopment && typeof window !== 'undefined') {
      console.group('⚠️ Application Warning');
      console.warn(message);
      if (data) console.warn('Context:', data);
      console.groupEnd();
    }
  }
  
  /**
   * Write an error-level message
   * @param message - The error message
   * @param data - Optional error details
   */
  public error(message: string, data?: any): void {
    console.error(`[ERROR] ${message}`, data || '');
    
    // Make errors more visible in development
    if (this.isDevelopment && typeof window !== 'undefined') {
      console.group('🚨 Application Error');
      console.error(message);
      if (data) console.error('Details:', data);
      console.groupEnd();
    }
    
    // TODO: Send to error tracking service in production
  }
  
  /**
   * Write a critical-level message for severe errors
   * @param message - The critical error message
   * @param data - Optional error details
   */
  public critical(message: string, data?: any): void {
    console.error(`[CRITICAL] ${message}`, data || '');
    
    // Make critical errors highly visible in development
    if (this.isDevelopment && typeof window !== 'undefined') {
      console.group('%c🔥 CRITICAL APPLICATION ERROR', 'color: red; font-weight: bold');
      console.error(message);
      if (data) console.error('Details:', data);
      console.trace('Stack trace:');
      console.groupEnd();
    }
    
    // TODO: Send to error tracking service and trigger alerts in production
  }
}

// Export singleton instance for application-wide use
export const logger = new LoggerService();

// React hook for component-level error logging
export function useLogger(): ILogger {
  return logger;
}