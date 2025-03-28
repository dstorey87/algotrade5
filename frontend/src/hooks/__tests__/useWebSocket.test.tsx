/**
 * Test Suite for useWebSocket Hook
 * 
 * Tests WebSocket hook functionality including:
 * - Connection lifecycle
 * - State management
 * - Error handling
 * - Cleanup behavior
 */

import { renderHook, act } from '@testing-library/react';
import { useWebSocket } from '../useWebSocket';
import { WebSocketService, WSEventType, ConnectionState } from '../../services/WebSocketService';
import { logger } from '@/src/utils/logger';

// Mock the WebSocket service
jest.mock('../../services/WebSocketService');
jest.mock('@/src/utils/logger');

describe('useWebSocket', () => {
  // Mock implementation
  const mockSubscribe = jest.fn();
  const mockSend = jest.fn();
  const mockConnect = jest.fn();
  const mockDisconnect = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Setup WebSocketService mock
    (WebSocketService as jest.Mock).mockImplementation(() => ({
      subscribe: mockSubscribe,
      send: mockSend,
      connect: mockConnect,
      disconnect: mockDisconnect
    }));

    // Return unsubscribe function from subscribe
    mockSubscribe.mockReturnValue(() => {});
  });

  it('should initialize WebSocket connection on mount', () => {
    renderHook(() => useWebSocket());

    expect(WebSocketService).toHaveBeenCalled();
    expect(mockConnect).toHaveBeenCalled();
    expect(logger.info).toHaveBeenCalledWith(
      'Initializing WebSocket hook',
      expect.any(Object)
    );
  });

  it('should handle WebSocket subscription', () => {
    const { result } = renderHook(() => useWebSocket());
    const mockHandler = jest.fn();

    act(() => {
      result.current.subscribe(WSEventType.TRADE_UPDATE, mockHandler);
    });

    expect(mockSubscribe).toHaveBeenCalledWith(
      WSEventType.TRADE_UPDATE,
      mockHandler
    );
    expect(logger.debug).toHaveBeenCalledWith(
      'Component subscribing to WebSocket event',
      expect.any(Object)
    );
  });

  it('should handle sending messages', () => {
    const { result } = renderHook(() => useWebSocket());
    const payload = { data: 'test' };

    act(() => {
      result.current.send(WSEventType.TRADE_UPDATE, payload);
    });

    expect(mockSend).toHaveBeenCalledWith(WSEventType.TRADE_UPDATE, payload);
  });

  it('should warn when trying to send before initialization', () => {
    // Simulate uninitialized state
    (WebSocketService as jest.Mock).mockImplementation(() => null);

    const { result } = renderHook(() => useWebSocket());
    const payload = { data: 'test' };

    act(() => {
      result.current.send(WSEventType.TRADE_UPDATE, payload);
    });

    expect(logger.warn).toHaveBeenCalledWith(
      'Attempted to send message before WebSocket initialization',
      expect.any(Object)
    );
  });

  it('should warn when trying to subscribe before initialization', () => {
    // Simulate uninitialized state
    (WebSocketService as jest.Mock).mockImplementation(() => null);

    const { result } = renderHook(() => useWebSocket());
    const mockHandler = jest.fn();

    act(() => {
      result.current.subscribe(WSEventType.TRADE_UPDATE, mockHandler);
    });

    expect(logger.warn).toHaveBeenCalledWith(
      'Attempted to subscribe before WebSocket initialization',
      expect.any(Object)
    );
  });

  it('should cleanup WebSocket connection on unmount', () => {
    const { unmount } = renderHook(() => useWebSocket());

    unmount();

    expect(mockDisconnect).toHaveBeenCalled();
    expect(logger.info).toHaveBeenCalledWith(
      'Cleaning up WebSocket hook',
      expect.any(Object)
    );
  });

  it('should handle connection state updates', () => {
    // Setup mock to simulate connection state changes
    mockSubscribe.mockImplementation((type, handler) => {
      if (type === WSEventType.SYSTEM_STATUS) {
        handler({ connectionState: ConnectionState.CONNECTED });
      }
      return () => {};
    });

    const { result } = renderHook(() => useWebSocket());

    expect(result.current.connectionState).toBe(ConnectionState.CONNECTED);
  });

  it('should handle initialization errors', () => {
    const mockError = new Error('Initialization failed');
    (WebSocketService as jest.Mock).mockImplementation(() => {
      throw mockError;
    });

    renderHook(() => useWebSocket());

    expect(logger.error).toHaveBeenCalledWith(
      'Failed to initialize WebSocket hook',
      expect.objectContaining({
        error: expect.objectContaining({
          message: mockError.message
        })
      })
    );
  });
});