/**
 * WebSocket Hook for AlgoTradePro5
 * 
 * Provides React components with WebSocket functionality:
 * - Connection management
 * - Real-time data subscription
 * - Error handling
 * - Auto-reconnection
 * 
 * @example
 * ```tsx
 * function TradeComponent() {
 *   const { 
 *     subscribe, 
 *     send, 
 *     connectionState 
 *   } = useWebSocket();
 * 
 *   useEffect(() => {
 *     const unsubscribe = subscribe(WSEventType.TRADE_UPDATE, handleTrade);
 *     return () => unsubscribe();
 *   }, []);
 * }
 * ```
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { WebSocketService, WSEventType, ConnectionState } from '../services/WebSocketService';
import { logger } from '@/src/utils/logger';

// Load WebSocket configuration from environment variables
const WS_CONFIG = {
  url: process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8080',
  reconnectInterval: Number(process.env.NEXT_PUBLIC_WS_RECONNECT_INTERVAL) || 5000,
  maxReconnectAttempts: Number(process.env.NEXT_PUBLIC_WS_MAX_RECONNECT_ATTEMPTS) || 5
};

/**
 * Hook for managing WebSocket connections in React components
 * @returns WebSocket management functions and state
 */
export function useWebSocket() {
  // Maintain WebSocket service instance across renders
  const wsRef = useRef<WebSocketService | null>(null);
  
  // Track connection state for UI updates
  const [connectionState, setConnectionState] = useState<ConnectionState>(
    ConnectionState.DISCONNECTED
  );

  /**
   * Initialize WebSocket service
   */
  const initializeWebSocket = useCallback(() => {
    try {
      if (!wsRef.current) {
        logger.info('Initializing WebSocket hook', {
          config: WS_CONFIG,
          timestamp: new Date().toISOString()
        });

        wsRef.current = new WebSocketService(WS_CONFIG);
        
        // Subscribe to connection state changes
        wsRef.current.subscribe(WSEventType.SYSTEM_STATUS, (status) => {
          setConnectionState(status.connectionState);
        });

        wsRef.current.connect();
      }
    } catch (error) {
      logger.error('Failed to initialize WebSocket hook', {
        error: error instanceof Error ? {
          message: error.message,
          stack: error.stack
        } : error,
        timestamp: new Date().toISOString()
      });
    }
  }, []);

  /**
   * Subscribe to WebSocket events
   */
  const subscribe = useCallback(<T = any>(
    type: WSEventType,
    handler: (data: T) => void
  ) => {
    if (!wsRef.current) {
      logger.warn('Attempted to subscribe before WebSocket initialization', {
        eventType: type,
        timestamp: new Date().toISOString()
      });
      return () => {};
    }

    logger.debug('Component subscribing to WebSocket event', {
      type,
      timestamp: new Date().toISOString()
    });

    return wsRef.current.subscribe(type, handler);
  }, []);

  /**
   * Send message through WebSocket
   */
  const send = useCallback((type: WSEventType, payload: any) => {
    if (!wsRef.current) {
      logger.warn('Attempted to send message before WebSocket initialization', {
        eventType: type,
        timestamp: new Date().toISOString()
      });
      return;
    }

    wsRef.current.send(type, payload);
  }, []);

  /**
   * Initialize WebSocket on mount
   */
  useEffect(() => {
    initializeWebSocket();

    // Cleanup on unmount
    return () => {
      logger.info('Cleaning up WebSocket hook', {
        timestamp: new Date().toISOString()
      });
      
      wsRef.current?.disconnect();
      wsRef.current = null;
    };
  }, [initializeWebSocket]);

  return {
    subscribe,
    send,
    connectionState
  };
}