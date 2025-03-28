import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { WebSocketErrorBoundary } from '../WebSocketErrorBoundary';
import '@testing-library/jest-dom';
import { logger } from '@/src/utils/logger';

// Mock the logger to verify logging calls
jest.mock('@/src/utils/logger', () => ({
  logger: {
    error: jest.fn(),
    critical: jest.fn(),
    info: jest.fn(),
    debug: jest.fn(),
  },
}));

/**
 * Test suite for WebSocketErrorBoundary component
 * 
 * Tests error handling, logging, and retry functionality of the WebSocket error boundary
 */
describe('WebSocketErrorBoundary', () => {
  // Reset all mocks before each test
  beforeEach(() => {
    jest.clearAllMocks();
  });

  /**
   * Helper function to simulate an error in a child component
   */
  const ErrorComponent = ({ shouldThrow = false }) => {
    if (shouldThrow) {
      throw new Error('Test WebSocket error');
    }
    return <div>Child Component</div>;
  };

  it('renders children when there is no error', () => {
    render(
      <WebSocketErrorBoundary>
        <div>Test Child</div>
      </WebSocketErrorBoundary>
    );

    expect(screen.getByText('Test Child')).toBeInTheDocument();
  });

  it('displays error UI when an error occurs', () => {
    // Suppress console.error for this test as we expect an error
    const originalError = console.error;
    console.error = jest.fn();

    render(
      <WebSocketErrorBoundary>
        <ErrorComponent shouldThrow={true} />
      </WebSocketErrorBoundary>
    );

    // Verify error UI elements
    expect(screen.getByText('Connection Error')).toBeInTheDocument();
    expect(screen.getByText('Test WebSocket error')).toBeInTheDocument();
    expect(screen.getByText('RETRY CONNECTION')).toBeInTheDocument();

    // Verify logger was called with error
    expect(logger.error).toHaveBeenCalledWith(
      'WebSocket error caught in boundary',
      expect.objectContaining({
        error: 'Test WebSocket error',
      })
    );

    // Restore console.error
    console.error = originalError;
  });

  it('handles retry button click', async () => {
    // Suppress console.error for this test as we expect an error
    const originalError = console.error;
    console.error = jest.fn();

    render(
      <WebSocketErrorBoundary>
        <ErrorComponent shouldThrow={true} />
      </WebSocketErrorBoundary>
    );

    // Click retry button
    const retryButton = screen.getByTestId('websocket-retry-button');
    await act(async () => {
      fireEvent.click(retryButton);
    });

    // Verify logging calls
    expect(logger.info).toHaveBeenCalledWith(
      'Attempting WebSocket reconnection',
      expect.objectContaining({
        previousError: 'Test WebSocket error',
      })
    );

    expect(logger.debug).toHaveBeenCalledWith(
      'WebSocket error state reset',
      expect.any(Object)
    );

    // Restore console.error
    console.error = originalError;
  });

  it('shows component stack in development mode', () => {
    // Set NODE_ENV to development
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'development';

    // Suppress console.error
    const originalError = console.error;
    console.error = jest.fn();

    render(
      <WebSocketErrorBoundary>
        <ErrorComponent shouldThrow={true} />
      </WebSocketErrorBoundary>
    );

    // Verify component stack is visible
    const errorInfo = screen.getByText(/at ErrorComponent/);
    expect(errorInfo).toBeInTheDocument();

    // Restore environment and console.error
    process.env.NODE_ENV = originalEnv;
    console.error = originalError;
  });

  it('logs critical errors with full stack trace', () => {
    // Suppress console.error
    const originalError = console.error;
    console.error = jest.fn();

    render(
      <WebSocketErrorBoundary>
        <ErrorComponent shouldThrow={true} />
      </WebSocketErrorBoundary>
    );

    // Verify critical error logging
    expect(logger.critical).toHaveBeenCalledWith(
      'WebSocket Error Boundary caught an error',
      expect.objectContaining({
        error: expect.objectContaining({
          message: 'Test WebSocket error',
          type: 'Error',
        }),
        componentStack: expect.any(String),
      })
    );

    // Restore console.error
    console.error = originalError;
  });
});