/**
 * WebSocket Service for AlgoTradePro5
 * 
 * Handles real-time communication with the trading system:
 * - Trade updates
 * - Strategy performance metrics
 * - System health monitoring
 * - Error reporting
 * 
 * Features:
 * - Automatic reconnection
 * - Event-based message handling
 * - Comprehensive error logging
 * - Performance monitoring
 */

import { logger } from '@/src/utils/logger';

// WebSocket event types
export enum WSEventType {
  TRADE_UPDATE = 'trade_update',
  STRATEGY_UPDATE = 'strategy_update',
  SYSTEM_STATUS = 'system_status',
  ERROR = 'error'
}

// WebSocket message interface
export interface WSMessage {
  type: WSEventType;
  payload: any;
  timestamp: string;
}

// WebSocket connection states
export enum ConnectionState {
  CONNECTING = 'connecting',
  CONNECTED = 'connected',
  DISCONNECTED = 'disconnected',
  ERROR = 'error'
}

/**
 * WebSocket connection configuration
 */
interface WSConfig {
  url: string;
  reconnectInterval: number;
  maxReconnectAttempts: number;
}

/**
 * WebSocket Service Class
 * Manages WebSocket connections and message handling
 */
export class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private messageHandlers: Map<WSEventType, ((message: any) => void)[]> = new Map();
  private connectionState: ConnectionState = ConnectionState.DISCONNECTED;
  private reconnectTimer: NodeJS.Timeout | null = null;

  constructor(private config: WSConfig) {
    // Initialize handlers map for each event type
    Object.values(WSEventType).forEach(type => {
      this.messageHandlers.set(type as WSEventType, []);
    });
  }

  /**
   * Initialize WebSocket connection
   */
  public connect(): void {
    logger.info('Initializing WebSocket connection', {
      url: this.config.url,
      timestamp: new Date().toISOString()
    });

    try {
      this.connectionState = ConnectionState.CONNECTING;
      this.ws = new WebSocket(this.config.url);
      this.setupEventHandlers();
    } catch (error) {
      this.handleError('Failed to initialize WebSocket', error);
    }
  }

  /**
   * Set up WebSocket event handlers
   */
  private setupEventHandlers(): void {
    if (!this.ws) return;

    this.ws.onopen = () => {
      this.connectionState = ConnectionState.CONNECTED;
      this.reconnectAttempts = 0;
      logger.info('WebSocket connected successfully', {
        timestamp: new Date().toISOString()
      });
    };

    this.ws.onmessage = (event: MessageEvent) => {
      try {
        const message: WSMessage = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        this.handleError('Failed to parse WebSocket message', error);
      }
    };

    this.ws.onclose = () => {
      this.connectionState = ConnectionState.DISCONNECTED;
      logger.warn('WebSocket connection closed', {
        reconnectAttempts: this.reconnectAttempts,
        timestamp: new Date().toISOString()
      });
      this.attemptReconnection();
    };

    this.ws.onerror = (error) => {
      this.handleError('WebSocket error occurred', error);
    };
  }

  /**
   * Handle incoming WebSocket messages
   */
  private handleMessage(message: WSMessage): void {
    const handlers = this.messageHandlers.get(message.type) || [];
    
    logger.debug('Received WebSocket message', {
      type: message.type,
      timestamp: message.timestamp
    });

    handlers.forEach(handler => {
      try {
        handler(message.payload);
      } catch (error) {
        this.handleError('Error in message handler', error);
      }
    });
  }

  /**
   * Send message through WebSocket
   */
  public send(type: WSEventType, payload: any): void {
    if (this.connectionState !== ConnectionState.CONNECTED) {
      logger.warn('Attempted to send message while disconnected', {
        type,
        timestamp: new Date().toISOString()
      });
      return;
    }

    try {
      const message: WSMessage = {
        type,
        payload,
        timestamp: new Date().toISOString()
      };

      this.ws?.send(JSON.stringify(message));
      
      logger.debug('Sent WebSocket message', {
        type,
        timestamp: message.timestamp
      });
    } catch (error) {
      this.handleError('Failed to send WebSocket message', error);
    }
  }

  /**
   * Subscribe to WebSocket events
   */
  public subscribe(type: WSEventType, handler: (message: any) => void): () => void {
    const handlers = this.messageHandlers.get(type) || [];
    handlers.push(handler);
    this.messageHandlers.set(type, handlers);

    logger.debug('Subscribed to WebSocket event', {
      type,
      handlersCount: handlers.length,
      timestamp: new Date().toISOString()
    });

    // Return unsubscribe function
    return () => {
      const currentHandlers = this.messageHandlers.get(type) || [];
      const index = currentHandlers.indexOf(handler);
      if (index > -1) {
        currentHandlers.splice(index, 1);
        this.messageHandlers.set(type, currentHandlers);
        
        logger.debug('Unsubscribed from WebSocket event', {
          type,
          handlersCount: currentHandlers.length,
          timestamp: new Date().toISOString()
        });
      }
    };
  }

  /**
   * Attempt to reconnect to WebSocket
   */
  private attemptReconnection(): void {
    if (this.reconnectAttempts >= this.config.maxReconnectAttempts) {
      this.connectionState = ConnectionState.ERROR;
      logger.error('Max reconnection attempts reached', {
        attempts: this.reconnectAttempts,
        timestamp: new Date().toISOString()
      });
      return;
    }

    this.reconnectAttempts++;
    logger.info('Attempting WebSocket reconnection', {
      attempt: this.reconnectAttempts,
      maxAttempts: this.config.maxReconnectAttempts,
      timestamp: new Date().toISOString()
    });

    this.reconnectTimer = setTimeout(() => {
      this.connect();
    }, this.config.reconnectInterval);
  }

  /**
   * Handle WebSocket errors
   */
  private handleError(message: string, error: any): void {
    this.connectionState = ConnectionState.ERROR;
    
    logger.error(message, {
      error: error instanceof Error ? {
        message: error.message,
        stack: error.stack
      } : error,
      timestamp: new Date().toISOString()
    });

    // Notify error handlers
    const errorHandlers = this.messageHandlers.get(WSEventType.ERROR) || [];
    errorHandlers.forEach(handler => {
      try {
        handler(error);
      } catch (handlerError) {
        logger.critical('Error in error handler', {
          originalError: error,
          handlerError,
          timestamp: new Date().toISOString()
        });
      }
    });
  }

  /**
   * Clean up WebSocket connection
   */
  public disconnect(): void {
    logger.info('Disconnecting WebSocket', {
      timestamp: new Date().toISOString()
    });

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.connectionState = ConnectionState.DISCONNECTED;
  }

  /**
   * Get current connection state
   */
  public getState(): ConnectionState {
    return this.connectionState;
  }
}