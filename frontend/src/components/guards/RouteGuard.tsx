/**
 * Route Guard Component
 * 
 * Protects routes based on authentication state and access level.
 * Features:
 * - Authentication verification
 * - Role-based access control
 * - Redirect handling
 * - Loading states
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { CircularProgress, Box } from '@mui/material';
import { findRouteByPath, RouteAccess } from '@/src/utils/routes';
import { logger } from '@/src/utils/logger';

interface RouteGuardProps {
  children: React.ReactNode;
}

export function RouteGuard({ children }: RouteGuardProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    checkAuthorization();
  }, [pathname]);

  /**
   * Check if current user is authorized to access the route
   */
  const checkAuthorization = async () => {
    try {
      setIsLoading(true);

      // Find route configuration for current path
      const route = findRouteByPath(pathname);

      if (!route) {
        logger.warn('Route not found in configuration', {
          pathname,
          timestamp: new Date().toISOString()
        });
        handleUnauthorized();
        return;
      }

      // Check route access requirements
      if (route.access === RouteAccess.PUBLIC) {
        setIsAuthorized(true);
        return;
      }

      // Verify authentication status
      const isAuthenticated = await verifyAuthentication();

      if (!isAuthenticated) {
        logger.info('User not authenticated, redirecting to login', {
          pathname,
          timestamp: new Date().toISOString()
        });
        handleUnauthorized();
        return;
      }

      // Check admin access if required
      if (route.access === RouteAccess.ADMIN) {
        const isAdmin = await verifyAdminAccess();
        if (!isAdmin) {
          logger.warn('User not authorized for admin route', {
            pathname,
            timestamp: new Date().toISOString()
          });
          handleUnauthorized();
          return;
        }
      }

      // Authorization successful
      setIsAuthorized(true);
      logger.debug('Route access authorized', {
        pathname,
        routeAccess: route.access,
        timestamp: new Date().toISOString()
      });

    } catch (error) {
      logger.error('Error checking route authorization', {
        error: error instanceof Error ? {
          message: error.message,
          stack: error.stack
        } : error,
        pathname,
        timestamp: new Date().toISOString()
      });
      handleUnauthorized();
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Verify user authentication status
   */
  const verifyAuthentication = async (): Promise<boolean> => {
    try {
      // Add your authentication verification logic here
      // For example, checking JWT token validity
      const token = localStorage.getItem('auth_token');
      
      if (!token) {
        return false;
      }

      // Verify token with backend
      const response = await fetch('/api/auth/verify', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      return response.ok;

    } catch (error) {
      logger.error('Authentication verification failed', {
        error: error instanceof Error ? {
          message: error.message,
          stack: error.stack
        } : error,
        timestamp: new Date().toISOString()
      });
      return false;
    }
  };

  /**
   * Verify admin access rights
   */
  const verifyAdminAccess = async (): Promise<boolean> => {
    try {
      const token = localStorage.getItem('auth_token');
      
      if (!token) {
        return false;
      }

      // Verify admin status with backend
      const response = await fetch('/api/auth/verify-admin', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      return response.ok;

    } catch (error) {
      logger.error('Admin verification failed', {
        error: error instanceof Error ? {
          message: error.message,
          stack: error.stack
        } : error,
        timestamp: new Date().toISOString()
      });
      return false;
    }
  };

  /**
   * Handle unauthorized access
   */
  const handleUnauthorized = () => {
    setIsAuthorized(false);
    // Save attempted URL for redirect after login
    localStorage.setItem('redirect_url', pathname);
    router.push('/auth/login');
  };

  /**
   * Render loading state
   */
  if (isLoading) {
    return (
      <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  /**
   * Render children only if authorized
   */
  return isAuthorized ? <>{children}</> : null;
}