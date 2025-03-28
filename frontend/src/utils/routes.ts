/**
 * Route Configuration Utility for AlgoTradePro5
 * 
 * Centralizes route management with:
 * - Type-safe route definitions
 * - Access control configuration
 * - Navigation helpers
 * - Route metadata for analytics
 */

import { logger } from './logger';

/**
 * Route access levels for authorization
 */
export enum RouteAccess {
  PUBLIC = 'public',
  PROTECTED = 'protected',
  ADMIN = 'admin'
}

/**
 * Route metadata interface
 */
interface RouteMetadata {
  title: string;
  description: string;
  access: RouteAccess;
  analyticsId?: string;
}

/**
 * Route configuration interface
 */
interface RouteConfig extends RouteMetadata {
  path: string;
  component?: string;
  redirectTo?: string;
  children?: Record<string, RouteConfig>;
}

/**
 * Application route configuration
 */
export const routes: Record<string, RouteConfig> = {
  home: {
    path: '/',
    title: 'Dashboard',
    description: 'AI-driven trading dashboard with real-time metrics',
    access: RouteAccess.PROTECTED,
    analyticsId: 'dashboard_view'
  },
  strategies: {
    path: '/strategies',
    title: 'Trading Strategies',
    description: 'View and manage AI trading strategies',
    access: RouteAccess.PROTECTED,
    children: {
      list: {
        path: '/strategies',
        title: 'All Strategies',
        description: 'List of all available trading strategies',
        access: RouteAccess.PROTECTED,
        analyticsId: 'strategy_list'
      },
      create: {
        path: '/strategies/create',
        title: 'Create Strategy',
        description: 'Create a new trading strategy',
        access: RouteAccess.PROTECTED,
        analyticsId: 'strategy_create'
      },
      detail: {
        path: '/strategies/:id',
        title: 'Strategy Details',
        description: 'View strategy performance and settings',
        access: RouteAccess.PROTECTED,
        analyticsId: 'strategy_detail'
      }
    }
  },
  trades: {
    path: '/trades',
    title: 'Trade History',
    description: 'View trading history and performance',
    access: RouteAccess.PROTECTED,
    children: {
      active: {
        path: '/trades/active',
        title: 'Active Trades',
        description: 'Currently open trading positions',
        access: RouteAccess.PROTECTED,
        analyticsId: 'trades_active'
      },
      history: {
        path: '/trades/history',
        title: 'Trade History',
        description: 'Historical trading performance',
        access: RouteAccess.PROTECTED,
        analyticsId: 'trades_history'
      }
    }
  },
  quantum: {
    path: '/quantum',
    title: 'Quantum Analysis',
    description: 'Quantum loop backtesting and optimization',
    access: RouteAccess.PROTECTED,
    children: {
      dashboard: {
        path: '/quantum/dashboard',
        title: 'Quantum Dashboard',
        description: 'Real-time quantum loop performance',
        access: RouteAccess.PROTECTED,
        analyticsId: 'quantum_dashboard'
      },
      optimize: {
        path: '/quantum/optimize',
        title: 'Strategy Optimization',
        description: 'Run quantum optimization on strategies',
        access: RouteAccess.PROTECTED,
        analyticsId: 'quantum_optimize'
      }
    }
  },
  settings: {
    path: '/settings',
    title: 'System Settings',
    description: 'Configure trading parameters and preferences',
    access: RouteAccess.ADMIN,
    analyticsId: 'settings_view'
  }
};

/**
 * Type for route parameters
 */
type RouteParams = Record<string, string | number>;

/**
 * Generate URL with parameters
 */
export function generateUrl(route: RouteConfig, params?: RouteParams): string {
  try {
    if (!route.path) {
      throw new Error('Route path is required');
    }

    let url = route.path;

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url = url.replace(`:${key}`, String(value));
      });
    }

    // Log URL generation for debugging
    logger.debug('Generated route URL', {
      originalPath: route.path,
      params,
      generatedUrl: url,
      timestamp: new Date().toISOString()
    });

    return url;
  } catch (error) {
    logger.error('Failed to generate route URL', {
      error: error instanceof Error ? {
        message: error.message,
        stack: error.stack
      } : error,
      route,
      params,
      timestamp: new Date().toISOString()
    });
    return route.path; // Return original path on error
  }
}

/**
 * Check if a route requires authentication
 */
export function isProtectedRoute(route: RouteConfig): boolean {
  return route.access !== RouteAccess.PUBLIC;
}

/**
 * Find route configuration by path
 */
export function findRouteByPath(path: string): RouteConfig | null {
  try {
    // Normalize the path
    const normalizedPath = path.toLowerCase();

    // Helper function to search through route tree
    const searchRoutes = (routes: Record<string, RouteConfig>): RouteConfig | null => {
      for (const key in routes) {
        const route = routes[key];
        
        // Check if this is the route we're looking for
        if (route.path.toLowerCase() === normalizedPath) {
          return route;
        }
        
        // Check children if they exist
        if (route.children) {
          const childRoute = searchRoutes(route.children);
          if (childRoute) {
            return childRoute;
          }
        }
      }
      return null;
    };

    const route = searchRoutes(routes);

    if (!route) {
      logger.debug('Route not found', {
        searchPath: path,
        timestamp: new Date().toISOString()
      });
    }

    return route;
  } catch (error) {
    logger.error('Error finding route by path', {
      error: error instanceof Error ? {
        message: error.message,
        stack: error.stack
      } : error,
      path,
      timestamp: new Date().toISOString()
    });
    return null;
  }
}