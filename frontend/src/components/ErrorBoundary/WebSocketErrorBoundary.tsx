'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { Box, Alert, AlertTitle, Button } from '@mui/material';
import { logger } from '@/src/utils/logger';

/**
 * Interface for WebSocketErrorBoundary props
 * @interface Props
 * @property {ReactNode} children - Child components to be wrapped by the error boundary
 */
interface Props {
  children: ReactNode;
}

/**
 * Interface for WebSocketErrorBoundary state
 * @interface State
 * @property {boolean} hasError - Flag indicating if an error has occurred
 * @property {Error | null} error - The error object if one exists
 * @property {ErrorInfo | null} errorInfo - React error info object containing component stack
 */
interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * WebSocketErrorBoundary Component
 * 
 * Handles WebSocket connection errors and provides a user-friendly error UI with retry functionality.
 * Implements React's Error Boundary pattern to catch and handle errors in child components.
 * 
 * Features:
 * - Catches and logs WebSocket related errors
 * - Provides a retry mechanism for failed connections
 * - Displays user-friendly error messages
 * - Integrates with the application's logging system
 * 
 * @extends {Component<Props, State>}
 */
export class WebSocketErrorBoundary extends Component<Props, State> {
  /**
   * Initialize component state
   * @type {State}
   */
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null
  };

  /**
   * Static method to derive error state from caught errors
   * @param {Error} error - The error that was caught
   * @returns {State} New state object with error information
   */
  public static getDerivedStateFromError(error: Error): State {
    // Log the error when it's first caught
    logger.error('WebSocket error caught in boundary', {
      error: error.message,
      stack: error.stack,
      timestamp: new Date().toISOString()
    });

    return { hasError: true, error, errorInfo: null };
  }

  /**
   * Lifecycle method called when an error occurs in a child component
   * @param {Error} error - The error that was caught
   * @param {ErrorInfo} errorInfo - React error info object with component stack
   */
  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log detailed error information
    logger.critical('WebSocket Error Boundary caught an error', {
      error: {
        message: error.message,
        stack: error.stack,
        type: error.name
      },
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString()
    });

    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  /**
   * Handles retry attempts for WebSocket connections
   * Resets error state and triggers reconnection
   */
  private handleRetry = () => {
    logger.info('Attempting WebSocket reconnection', {
      timestamp: new Date().toISOString(),
      previousError: this.state.error?.message
    });

    this.setState({ hasError: false, error: null, errorInfo: null });

    // Log the retry attempt
    logger.debug('WebSocket error state reset', {
      timestamp: new Date().toISOString()
    });
  };

  /**
   * Renders either the error UI or the wrapped children
   * @returns {ReactNode} The rendered component
   */
  public render(): ReactNode {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
          <Alert 
            severity="error" 
            action={
              <Button 
                color="inherit" 
                size="small" 
                onClick={this.handleRetry}
                data-testid="websocket-retry-button"
              >
                RETRY CONNECTION
              </Button>
            }
          >
            <AlertTitle>Connection Error</AlertTitle>
            {this.state.error?.message || 'Failed to connect to trading server'}
            {process.env.NODE_ENV === 'development' && (
              <Box sx={{ mt: 2, fontSize: '0.8rem', color: 'text.secondary' }}>
                {this.state.errorInfo?.componentStack}
              </Box>
            )}
          </Alert>
        </Box>
      );
    }

    return this.props.children;
  }
}