/**
 * Root Routes Configuration (Middleware)
 * 
 * Handles routing and request middleware for AlgoTradePro5 frontend.
 * Provides centralized routing control and logging for all requests.
 * 
 * Features:
 * - Request logging and debugging
 * - Route normalization
 * - Security headers
 * - Performance monitoring
 * 
 * @see https://nextjs.org/docs/app/building-your-application/routing
 */

// Polyfill fetch API for older browsers
import 'whatwg-fetch';
import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/src/utils/logger';

/**
 * Request timing symbol for performance tracking
 */
const REQUEST_START_TIME = Symbol('RequestStartTime');

/**
 * Middleware function to handle all incoming requests
 * Provides routing control, logging, and request timing
 * 
 * @param {NextRequest} request - The incoming request object
 * @returns {NextResponse} The middleware response
 */
export function middleware(request: NextRequest) {
  // Start request timing
  const startTime = process.hrtime();
  (request as any)[REQUEST_START_TIME] = startTime;

  // Get request details
  const pathname = request.nextUrl.pathname;
  const method = request.method;
  const ip = request.ip || 'unknown';

  // Log incoming request
  logger.info('Incoming request', {
    pathname,
    method,
    ip,
    timestamp: new Date().toISOString(),
    headers: Object.fromEntries(request.headers),
  });

  try {
    // Handle root path
    if (pathname === '/') {
      logger.debug('Processing root route request', {
        originalUrl: request.url,
      });

      // Create normalized URL for the App Router home page
      const url = request.nextUrl.clone();
      
      // Important: We keep the URL as '/' but ensure it's handled by app/page.tsx
      // This maintains a clean URL while fixing the routing
      return NextResponse.rewrite(new URL('/', request.url));
    }

    // Add security headers to all responses
    const response = NextResponse.next();
    response.headers.set('X-Frame-Options', 'DENY');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

    // Log response timing
    const endTime = process.hrtime(startTime);
    const duration = Math.round((endTime[0] * 1000) + (endTime[1] / 1000000));
    
    logger.debug('Request completed', {
      pathname,
      duration: `${duration}ms`,
      timestamp: new Date().toISOString()
    });

    return response;

  } catch (error) {
    // Log any errors that occur during middleware processing
    logger.error('Middleware error', {
      error: error instanceof Error ? {
        message: error.message,
        stack: error.stack
      } : error,
      pathname,
      timestamp: new Date().toISOString()
    });

    // Return a basic response to prevent the application from crashing
    return NextResponse.next();
  }
}

/**
 * Middleware configuration
 * Specifies which paths this middleware should run on
 */
export const config = {
  matcher: [
    // Match all paths
    '/(.*)',
    // Exclude static files and api routes from timing/logging
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ]
};