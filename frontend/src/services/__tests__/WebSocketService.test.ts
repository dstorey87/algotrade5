/**
 * WebSocketService Test Suite
 * 
 * Tests the WebSocket service functionality including:
 * - Connection management
 * - Message handling
 * - Error scenarios
 * - Reconnection logic
 */

import { WebSocketService, WSEventType, ConnectionState } from '../WebSocketService';
import { logger } from '@/src/utils/logger';

// Mock the logger
jest.mock('@/src/utils/logger', () => ({
  logger: {
    info: jest.fn(),
    debug: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
    critical: jest.fn(),
  },
}));

// Mock WebSocket implementation
class MockWebSocket {
  onopen: (() => void) | null = null;
  onmessage: ((event: any) => void) | null = null;
  onclose: (() => void) | null = null;
  onerror: ((error: any) => void) | null = null;
  readyState: number = WebSocket.CONNECTING;

  constructor(public url: string) {}

  close(): void {
    this.readyState = WebSocket.CLOSED;
    this.onclose?.();
  }

  send(data: string): void {
    // Simulate successful send
  }
}

// Mock global WebSocket
(global as any).WebSocket = MockWebSocket;

describe('WebSocketService', () => {
  let wsService: WebSocketService;
  let mockWs: MockWebSocket;
  
  const config = {
    url: 'ws://test-server:8080',
    reconnectInterval: 1000,
    maxReconnectAttempts: 3
  };

  beforeEach(() => {
    jest.clearAllMocks();
    wsService = new WebSocketService(config);
  });

  describe('Connection Management', () => {
    it('should establish connection successfully', () => {
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];
      mockWs.onopen?.();

      expect(logger.info).toHaveBeenCalledWith(
        'WebSocket connected successfully',
        expect.any(Object)
      );
      expect(wsService.getState()).toBe(ConnectionState.CONNECTED);
    });

    it('should handle connection errors', () => {
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];
      mockWs.onerror?.(new Error('Connection failed'));

      expect(logger.error).toHaveBeenCalledWith(
        'WebSocket error occurred',
        expect.any(Object)
      );
      expect(wsService.getState()).toBe(ConnectionState.ERROR);
    });

    it('should attempt reconnection on close', () => {
      jest.useFakeTimers();
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];
      mockWs.onclose?.();

      expect(logger.warn).toHaveBeenCalledWith(
        'WebSocket connection closed',
        expect.any(Object)
      );

      // Fast-forward through reconnect timer
      jest.advanceTimersByTime(config.reconnectInterval);

      expect(logger.info).toHaveBeenCalledWith(
        'Attempting WebSocket reconnection',
        expect.objectContaining({
          attempt: 1,
          maxAttempts: config.maxReconnectAttempts
        })
      );

      jest.useRealTimers();
    });
  });

  describe('Message Handling', () => {
    beforeEach(() => {
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];
      mockWs.onopen?.();
    });

    it('should handle incoming messages correctly', () => {
      const mockHandler = jest.fn();
      wsService.subscribe(WSEventType.TRADE_UPDATE, mockHandler);

      const mockMessage = {
        type: WSEventType.TRADE_UPDATE,
        payload: { trade: 'data' },
        timestamp: new Date().toISOString()
      };

      mockWs.onmessage?.({ data: JSON.stringify(mockMessage) });

      expect(mockHandler).toHaveBeenCalledWith(mockMessage.payload);
      expect(logger.debug).toHaveBeenCalledWith(
        'Received WebSocket message',
        expect.any(Object)
      );
    });

    it('should handle message parsing errors', () => {
      mockWs.onmessage?.({ data: 'invalid json' });

      expect(logger.error).toHaveBeenCalledWith(
        'Failed to parse WebSocket message',
        expect.any(Object)
      );
    });

    it('should handle multiple subscribers for same event', () => {
      const handler1 = jest.fn();
      const handler2 = jest.fn();

      wsService.subscribe(WSEventType.SYSTEM_STATUS, handler1);
      wsService.subscribe(WSEventType.SYSTEM_STATUS, handler2);

      const mockMessage = {
        type: WSEventType.SYSTEM_STATUS,
        payload: { status: 'online' },
        timestamp: new Date().toISOString()
      };

      mockWs.onmessage?.({ data: JSON.stringify(mockMessage) });

      expect(handler1).toHaveBeenCalledWith(mockMessage.payload);
      expect(handler2).toHaveBeenCalledWith(mockMessage.payload);
    });

    it('should unsubscribe handlers correctly', () => {
      const handler = jest.fn();
      const unsubscribe = wsService.subscribe(WSEventType.STRATEGY_UPDATE, handler);

      unsubscribe();

      const mockMessage = {
        type: WSEventType.STRATEGY_UPDATE,
        payload: { strategy: 'update' },
        timestamp: new Date().toISOString()
      };

      mockWs.onmessage?.({ data: JSON.stringify(mockMessage) });

      expect(handler).not.toHaveBeenCalled();
      expect(logger.debug).toHaveBeenCalledWith(
        'Unsubscribed from WebSocket event',
        expect.any(Object)
      );
    });
  });

  describe('Message Sending', () => {
    beforeEach(() => {
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];
      mockWs.onopen?.();
    });

    it('should send messages when connected', () => {
      const spy = jest.spyOn(mockWs, 'send');
      
      wsService.send(WSEventType.TRADE_UPDATE, { order: 'data' });

      expect(spy).toHaveBeenCalled();
      expect(logger.debug).toHaveBeenCalledWith(
        'Sent WebSocket message',
        expect.any(Object)
      );
    });

    it('should not send messages when disconnected', () => {
      wsService.disconnect();
      const spy = jest.spyOn(mockWs, 'send');
      
      wsService.send(WSEventType.TRADE_UPDATE, { order: 'data' });

      expect(spy).not.toHaveBeenCalled();
      expect(logger.warn).toHaveBeenCalledWith(
        'Attempted to send message while disconnected',
        expect.any(Object)
      );
    });
  });

  describe('Error Handling', () => {
    it('should handle max reconnection attempts', () => {
      jest.useFakeTimers();
      
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];

      // Simulate multiple connection failures
      for (let i = 0; i <= config.maxReconnectAttempts; i++) {
        mockWs.onclose?.();
        jest.advanceTimersByTime(config.reconnectInterval);
      }

      expect(logger.error).toHaveBeenCalledWith(
        'Max reconnection attempts reached',
        expect.any(Object)
      );
      expect(wsService.getState()).toBe(ConnectionState.ERROR);

      jest.useRealTimers();
    });

    it('should handle errors in message handlers', () => {
      const errorHandler = jest.fn();
      wsService.subscribe(WSEventType.ERROR, errorHandler);

      const handlerWithError = () => {
        throw new Error('Handler error');
      };

      wsService.subscribe(WSEventType.TRADE_UPDATE, handlerWithError);

      const mockMessage = {
        type: WSEventType.TRADE_UPDATE,
        payload: {},
        timestamp: new Date().toISOString()
      };

      mockWs.onmessage?.({ data: JSON.stringify(mockMessage) });

      expect(logger.error).toHaveBeenCalledWith(
        'Error in message handler',
        expect.any(Object)
      );
      expect(errorHandler).toHaveBeenCalled();
    });
  });

  describe('Cleanup', () => {
    it('should clean up resources on disconnect', () => {
      jest.useFakeTimers();
      
      wsService.connect();
      mockWs = (global as any).WebSocket.mock.instances[0];
      const spy = jest.spyOn(mockWs, 'close');

      wsService.disconnect();

      expect(spy).toHaveBeenCalled();
      expect(wsService.getState()).toBe(ConnectionState.DISCONNECTED);
      expect(logger.info).toHaveBeenCalledWith(
        'Disconnecting WebSocket',
        expect.any(Object)
      );

      jest.useRealTimers();
    });
  });
});