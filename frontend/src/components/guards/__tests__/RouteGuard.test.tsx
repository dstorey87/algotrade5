/**
 * Test Suite for RouteGuard Component
 * 
 * Tests authentication and authorization including:
 * - Public route access
 * - Protected route access
 * - Admin route access
 * - Loading states
 * - Error handling
 */

import { render, screen, waitFor, act } from '@testing-library/react';
import { RouteGuard } from '../RouteGuard';
import { findRouteByPath, RouteAccess } from '@/src/utils/routes';
import { logger } from '@/src/utils/logger';

// Mock dependencies
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
  usePathname: () => '/test-path',
}));

jest.mock('@/src/utils/routes', () => ({
  findRouteByPath: jest.fn(),
  RouteAccess: {
    PUBLIC: 'public',
    PROTECTED: 'protected',
    ADMIN: 'admin'
  }
}));

jest.mock('@/src/utils/logger', () => ({
  logger: {
    warn: jest.fn(),
    info: jest.fn(),
    debug: jest.fn(),
    error: jest.fn(),
  }
}));

// Mock fetch globally
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('RouteGuard', () => {
  // Mock local storage
  const mockLocalStorage = {
    getItem: jest.fn(),
    setItem: jest.fn(),
    clear: jest.fn()
  };
  
  Object.defineProperty(window, 'localStorage', {
    value: mockLocalStorage
  });

  beforeEach(() => {
    jest.clearAllMocks();
    mockLocalStorage.getItem.mockReturnValue(null);
    mockFetch.mockReset();
  });

  describe('Public Routes', () => {
    beforeEach(() => {
      (findRouteByPath as jest.Mock).mockReturnValue({
        path: '/public',
        access: RouteAccess.PUBLIC
      });
    });

    it('should allow access to public routes without authentication', async () => {
      render(
        <RouteGuard>
          <div>Public Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(screen.getByText('Public Content')).toBeInTheDocument();
      });

      expect(mockFetch).not.toHaveBeenCalled();
    });
  });

  describe('Protected Routes', () => {
    beforeEach(() => {
      (findRouteByPath as jest.Mock).mockReturnValue({
        path: '/protected',
        access: RouteAccess.PROTECTED
      });
    });

    it('should redirect to login when not authenticated', async () => {
      const mockRouter = { push: jest.fn() };
      (require('next/navigation') as any).useRouter = () => mockRouter;

      render(
        <RouteGuard>
          <div>Protected Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(mockRouter.push).toHaveBeenCalledWith('/auth/login');
      });

      expect(logger.info).toHaveBeenCalledWith(
        'User not authenticated, redirecting to login',
        expect.any(Object)
      );
    });

    it('should allow access when properly authenticated', async () => {
      mockLocalStorage.getItem.mockReturnValue('valid_token');
      mockFetch.mockResolvedValueOnce({ ok: true });

      render(
        <RouteGuard>
          <div>Protected Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(screen.getByText('Protected Content')).toBeInTheDocument();
      });

      expect(mockFetch).toHaveBeenCalledWith('/api/auth/verify', {
        headers: { Authorization: 'Bearer valid_token' }
      });
    });

    it('should handle authentication errors gracefully', async () => {
      mockLocalStorage.getItem.mockReturnValue('valid_token');
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      render(
        <RouteGuard>
          <div>Protected Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(logger.error).toHaveBeenCalledWith(
          'Authentication verification failed',
          expect.any(Object)
        );
      });
    });
  });

  describe('Admin Routes', () => {
    beforeEach(() => {
      (findRouteByPath as jest.Mock).mockReturnValue({
        path: '/admin',
        access: RouteAccess.ADMIN
      });
    });

    it('should verify admin access for admin routes', async () => {
      mockLocalStorage.getItem.mockReturnValue('valid_token');
      mockFetch
        .mockResolvedValueOnce({ ok: true }) // auth verify
        .mockResolvedValueOnce({ ok: true }); // admin verify

      render(
        <RouteGuard>
          <div>Admin Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(screen.getByText('Admin Content')).toBeInTheDocument();
      });

      expect(mockFetch).toHaveBeenCalledWith('/api/auth/verify-admin', {
        headers: { Authorization: 'Bearer valid_token' }
      });
    });

    it('should deny access when admin verification fails', async () => {
      mockLocalStorage.getItem.mockReturnValue('valid_token');
      mockFetch
        .mockResolvedValueOnce({ ok: true }) // auth verify
        .mockResolvedValueOnce({ ok: false }); // admin verify

      const mockRouter = { push: jest.fn() };
      (require('next/navigation') as any).useRouter = () => mockRouter;

      render(
        <RouteGuard>
          <div>Admin Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(mockRouter.push).toHaveBeenCalledWith('/auth/login');
      });

      expect(logger.warn).toHaveBeenCalledWith(
        'User not authorized for admin route',
        expect.any(Object)
      );
    });
  });

  describe('Loading State', () => {
    it('should show loading indicator during authorization check', async () => {
      mockLocalStorage.getItem.mockReturnValue('valid_token');
      mockFetch.mockImplementation(() => new Promise(() => {})); // Never resolves

      render(
        <RouteGuard>
          <div>Content</div>
        </RouteGuard>
      );

      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });
  });

  describe('Error Handling', () => {
    it('should handle missing route configuration', async () => {
      (findRouteByPath as jest.Mock).mockReturnValue(null);

      render(
        <RouteGuard>
          <div>Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(logger.warn).toHaveBeenCalledWith(
          'Route not found in configuration',
          expect.any(Object)
        );
      });
    });

    it('should save redirect URL when unauthorized', async () => {
      const testPath = '/test-path';
      (require('next/navigation') as any).usePathname = () => testPath;

      render(
        <RouteGuard>
          <div>Content</div>
        </RouteGuard>
      );

      await waitFor(() => {
        expect(mockLocalStorage.setItem).toHaveBeenCalledWith('redirect_url', testPath);
      });
    });
  });
});