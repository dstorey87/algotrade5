import { useState, useCallback, useRef, useEffect } from 'react';
import { WSMessage } from '@/types';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (message: WSMessage | WSMessage[]) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
  batchInterval?: number;
  enableCompression?: boolean;
}

export function useWebSocket({
  url,
  onMessage,
  reconnectAttempts = 5,
  reconnectInterval = 3000,
  batchInterval = 100,
  enableCompression = true
}: UseWebSocketOptions) {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const attempts = useRef(0);
  const messageQueue = useRef<WSMessage[]>([]);
  const batchTimeout = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING);

  // Connection management with exponential backoff
  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        attempts.current = 0;
        setReadyState(WebSocket.OPEN);
      };

      ws.onclose = () => {
        setIsConnected(false);
        setReadyState(WebSocket.CLOSED);
        
        // Implement exponential backoff for reconnection
        if (attempts.current < reconnectAttempts) {
          const delay = reconnectInterval * Math.pow(2, attempts.current);
          setTimeout(() => {
            attempts.current++;
            connect();
          }, delay);
        }
      };

      ws.onerror = (event) => {
        setError('WebSocket connection error');
        setReadyState(WebSocket.CLOSED);
        console.error('WebSocket error:', event);
      };

      // Enhanced message handling with batching and compression
      ws.onmessage = (event) => {
        try {
          const data = enableCompression ? 
            decompress(event.data) : 
            JSON.parse(event.data);
          
          messageQueue.current.push(data);

          if (!batchTimeout.current) {
            batchTimeout.current = setTimeout(() => {
              if (messageQueue.current.length > 0) {
                onMessage?.(messageQueue.current);
                messageQueue.current = [];
              }
              batchTimeout.current = null;
            }, batchInterval);
          }
        } catch (err) {
          console.error('Error processing WebSocket message:', err);
          setError('Failed to process message');
        }
      };

      setSocket(ws);
      return () => {
        ws.close();
        if (batchTimeout.current) {
          clearTimeout(batchTimeout.current);
          batchTimeout.current = null;
        }
      };
    } catch (err) {
      setError('Failed to create WebSocket connection');
      setReadyState(WebSocket.CLOSED);
      console.error('WebSocket connection error:', err);
    }
  }, [url, reconnectAttempts, reconnectInterval, batchInterval, enableCompression, onMessage]);

  // Initialize connection
  useEffect(() => {
    const cleanup = connect();
    return () => cleanup?.();
  }, [connect]);

  // Message compression helper
  const decompress = useCallback((data: string): WSMessage => {
    // Implement your compression algorithm here
    return JSON.parse(data);
  }, []);

  // Optimized send function with compression
  const sendMessage = useCallback((message: string | object) => {
    if (socket?.readyState === WebSocket.OPEN) {
      const data = typeof message === 'string' ? message : JSON.stringify(message);
      socket.send(enableCompression ? compress(data) : data);
    } else {
      console.warn('WebSocket is not connected');
    }
  }, [socket, enableCompression]);

  // Message compression helper
  const compress = useCallback((data: string): string => {
    // Implement your compression algorithm here
    return data;
  }, []);

  return {
    isConnected,
    error,
    sendMessage,
    readyState,
    messageQueue: messageQueue.current
  };
}