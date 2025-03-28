/**
 * Test Suite for Route Configuration Utility
 * 
 * Tests route management functionality including:
 * - URL generation
 * - Route protection checks
 * - Route finding
 * - Error handling
 */

import { routes, RouteAccess, generateUrl, isProtectedRoute, findRouteByPath } from '../routes';
import { logger } from '../logger';

// Mock the logger
jest.mock('../logger', () => ({
  logger: {
    debug: jest.fn(),
    error: jest.fn(),
  },
}));

describe('Route Configuration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Route Definitions', () => {
    it('should have required properties for all routes', () => {
      const validateRoute = (route: any) => {
        expect(route).toHaveProperty('path');
        expect(route).toHaveProperty('title');
        expect(route).toHaveProperty('description');
        expect(route).toHaveProperty('access');
        
        if (route.children) {
          Object.values(route.children).forEach(validateRoute);
        }
      };

      Object.values(routes).forEach(validateRoute);
    });

    it('should have valid access levels', () => {
      const validateAccess = (route: any) => {
        expect(Object.values(RouteAccess)).toContain(route.access);
        
        if (route.children) {
          Object.values(route.children).forEach(validateAccess);
        }
      };

      Object.values(routes).forEach(validateAccess);
    });
  });

  describe('URL Generation', () => {
    it('should generate correct URLs without parameters', () => {
      const url = generateUrl(routes.home);
      expect(url).toBe('/');
      expect(logger.debug).toHaveBeenCalledWith(
        'Generated route URL',
        expect.any(Object)
      );
    });

    it('should generate URLs with parameters', () => {
      const url = generateUrl(routes.strategies.children!.detail, { id: '123' });
      expect(url).toBe('/strategies/123');
    });

    it('should handle missing parameters gracefully', () => {
      const url = generateUrl(routes.strategies.children!.detail);
      expect(url).toBe('/strategies/:id');
    });

    it('should handle invalid routes', () => {
      const invalidRoute = { title: 'Invalid' };
      // @ts-ignore - Testing invalid input
      const url = generateUrl(invalidRoute);
      expect(logger.error).toHaveBeenCalledWith(
        'Failed to generate route URL',
        expect.any(Object)
      );
    });
  });

  describe('Route Protection', () => {
    it('should identify protected routes', () => {
      expect(isProtectedRoute(routes.home)).toBe(true);
      expect(isProtectedRoute(routes.strategies)).toBe(true);
    });

    it('should identify admin routes', () => {
      expect(isProtectedRoute(routes.settings)).toBe(true);
      expect(routes.settings.access).toBe(RouteAccess.ADMIN);
    });

    it('should handle public routes when they exist', () => {
      const publicRoute = {
        path: '/public',
        title: 'Public',
        description: 'Public route',
        access: RouteAccess.PUBLIC
      };
      expect(isProtectedRoute(publicRoute)).toBe(false);
    });
  });

  describe('Route Finding', () => {
    it('should find root level routes', () => {
      const route = findRouteByPath('/');
      expect(route).toBe(routes.home);
    });

    it('should find nested routes', () => {
      const route = findRouteByPath('/trades/active');
      expect(route).toBe(routes.trades.children?.active);
    });

    it('should handle case insensitive paths', () => {
      const route = findRouteByPath('/STRATEGIES');
      expect(route).toBeTruthy();
      expect(route?.path).toBe('/strategies');
    });

    it('should return null for non-existent routes', () => {
      const route = findRouteByPath('/not-found');
      expect(route).toBeNull();
      expect(logger.debug).toHaveBeenCalledWith(
        'Route not found',
        expect.any(Object)
      );
    });

    it('should handle errors during route search', () => {
      // Simulate an error by passing invalid input
      const route = findRouteByPath({} as any);
      expect(route).toBeNull();
      expect(logger.error).toHaveBeenCalledWith(
        'Error finding route by path',
        expect.any(Object)
      );
    });
  });

  describe('Route Analytics', () => {
    it('should have analytics IDs for important routes', () => {
      expect(routes.home.analyticsId).toBeDefined();
      expect(routes.strategies.children?.list.analyticsId).toBeDefined();
      expect(routes.trades.children?.active.analyticsId).toBeDefined();
    });
  });

  describe('Route Tree Structure', () => {
    it('should maintain proper parent-child relationships', () => {
      expect(routes.strategies.children?.list.path.startsWith(routes.strategies.path)).toBe(true);
      expect(routes.trades.children?.active.path.startsWith(routes.trades.path)).toBe(true);
      expect(routes.quantum.children?.dashboard.path.startsWith(routes.quantum.path)).toBe(true);
    });

    it('should have unique paths across all routes', () => {
      const paths = new Set<string>();
      
      const checkPath = (route: any) => {
        expect(paths.has(route.path)).toBe(false);
        paths.add(route.path);
        
        if (route.children) {
          Object.values(route.children).forEach(checkPath);
        }
      };

      Object.values(routes).forEach(checkPath);
    });
  });
});