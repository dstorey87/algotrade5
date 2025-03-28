/**
 * Fetch API utilities for AlgoTradePro5 frontend
 * 
 * This module provides standardized fetch wrappers with:
 * - Error handling
 * - Timeout support
 * - Automatic logging
 * - Request/response interceptors
 * - Retry logic for flaky connections
 */

// Import whatwg-fetch polyfill to ensure fetch is available in all browsers
import 'whatwg-fetch';
import { logger, ErrorCategory } from './logger';

// Default request timeout in milliseconds
const DEFAULT_TIMEOUT = 30000;

// Maximum number of retries for failed requests
const MAX_RETRIES = 3;

// Retry backoff factor (exponential)
const RETRY_BACKOFF_FACTOR = 1.5;

/**
 * Custom fetch error with additional context
 */
export class FetchError extends Error {
  public status?: number;
  public statusText?: string;
  public url: string;
  public method: string;
  public retryCount: number;

  constructor(message: string, options: { 
    url: string, 
    method: string, 
    status?: number, 
    statusText?: string,
    retryCount?: number
  }) {
    super(message);
    this.name = 'FetchError';
    this.url = options.url;
    this.method = options.method;
    this.status = options.status;
    this.statusText = options.statusText;
    this.retryCount = options.retryCount || 0;
  }
}

/**
 * Request options with additional parameters
 */
export interface EnhancedRequestInit extends RequestInit {
  timeout?: number;
  retries?: number;
}

/**
 * Create an AbortController with timeout
 * 
 * @param timeoutMs - Timeout in milliseconds
 * @returns AbortController and timeout ID
 */
function createTimeoutController(timeoutMs: number = DEFAULT_TIMEOUT): { 
  controller: AbortController, 
  timeoutId: number 
} {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);
  return { controller, timeoutId };
}

/**
 * Enhanced fetch with timeouts, retries and error handling
 * 
 * @param url - The URL to fetch
 * @param options - Enhanced fetch options including timeout and retries
 * @returns Promise with the fetch response
 */
export async function enhancedFetch(url: string, options: EnhancedRequestInit = {}): Promise<Response> {
  const { 
    timeout = DEFAULT_TIMEOUT, 
    retries = MAX_RETRIES,
    ...fetchOptions 
  } = options;
  
  const method = (options.method || 'GET').toUpperCase();
  let retryCount = 0;
  let lastError: Error | null = null;
  
  // Log the outgoing request
  logger.debug(`Outgoing ${method} request to: ${url}`);
  
  while (retryCount <= retries) {
    const { controller, timeoutId } = createTimeoutController(timeout);
    
    try {
      // Add abort signal to the fetch options
      const fetchWithTimeoutOptions = {
        ...fetchOptions,
        signal: controller.signal
      };
      
      // Execute the fetch request
      const response = await fetch(url, fetchWithTimeoutOptions);
      
      // Clear the timeout
      clearTimeout(timeoutId);
      
      // Log non-successful responses
      if (!response.ok) {
        const errorMessage = `HTTP Error ${response.status}: ${response.statusText}`;
        logger.error(errorMessage, {
          category: ErrorCategory.NETWORK,
          url,
          method,
          status: response.status,
          statusText: response.statusText
        });
        
        throw new FetchError(errorMessage, {
          url,
          method,
          status: response.status,
          statusText: response.statusText,
          retryCount
        });
      }
      
      // Log successful responses
      logger.debug(`${method} request to ${url} succeeded`, {
        status: response.status
      });
      
      return response;
      
    } catch (error) {
      // Clear the timeout
      clearTimeout(timeoutId);
      
      // Handle and log the error
      const isAbortError = error instanceof Error && error.name === 'AbortError';
      const errorMessage = isAbortError 
        ? `Request to ${url} timed out after ${timeout}ms`
        : `Request to ${url} failed: ${error instanceof Error ? error.message : String(error)}`;
        
      lastError = error instanceof Error ? error : new Error(String(error));
      
      // Log the error
      logger.warn(errorMessage, {
        category: ErrorCategory.NETWORK,
        url,
        method,
        isTimeout: isAbortError,
        retryCount,
        error: lastError
      });
      
      // Increment retry counter
      retryCount++;
      
      // Check if we should retry
      if (retryCount <= retries) {
        // Calculate backoff time with exponential backoff
        const backoffMs = Math.min(1000 * Math.pow(RETRY_BACKOFF_FACTOR, retryCount - 1), 10000);
        
        logger.debug(`Retrying request to ${url} (${retryCount}/${retries}) after ${backoffMs}ms`);
        
        // Wait for the backoff period
        await new Promise(resolve => setTimeout(resolve, backoffMs));
        
        // Continue to next retry
        continue;
      }
      
      // If all retries failed, throw the last error
      if (error instanceof FetchError) {
        throw error;
      } else {
        throw new FetchError(errorMessage, {
          url,
          method,
          retryCount: retryCount - 1
        });
      }
    }
  }
  
  // This should never be reached but is here for type safety
  throw lastError || new Error(`Failed to fetch ${url}`);
}

/**
 * GET request wrapper with JSON response parsing
 * 
 * @param url - The URL to fetch
 * @param options - Fetch options
 * @returns Promise with the parsed JSON data
 */
export async function fetchJson<T = any>(url: string, options: EnhancedRequestInit = {}): Promise<T> {
  const response = await enhancedFetch(url, {
    ...options,
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      ...options.headers
    }
  });
  
  return response.json();
}

/**
 * POST request wrapper with JSON payload and response
 * 
 * @param url - The URL to post to
 * @param data - The data to send (will be JSON stringified)
 * @param options - Fetch options
 * @returns Promise with the parsed JSON response
 */
export async function postJson<T = any, D = any>(
  url: string, 
  data: D, 
  options: EnhancedRequestInit = {}
): Promise<T> {
  const response = await enhancedFetch(url, {
    ...options,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
}

/**
 * PUT request wrapper with JSON payload and response
 * 
 * @param url - The URL to put to
 * @param data - The data to send (will be JSON stringified)
 * @param options - Fetch options
 * @returns Promise with the parsed JSON response
 */
export async function putJson<T = any, D = any>(
  url: string, 
  data: D, 
  options: EnhancedRequestInit = {}
): Promise<T> {
  const response = await enhancedFetch(url, {
    ...options,
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      ...options.headers
    },
    body: JSON.stringify(data)
  });
  
  return response.json();
}

/**
 * DELETE request wrapper with optional JSON response
 * 
 * @param url - The URL to delete
 * @param options - Fetch options
 * @returns Promise with the parsed JSON response (if available)
 */
export async function deleteRequest<T = any>(url: string, options: EnhancedRequestInit = {}): Promise<T | void> {
  const response = await enhancedFetch(url, {
    ...options,
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
      ...options.headers
    }
  });
  
  try {
    return await response.json();
  } catch (e) {
    // Some DELETE endpoints don't return JSON, so we return void in that case
    return;
  }
}