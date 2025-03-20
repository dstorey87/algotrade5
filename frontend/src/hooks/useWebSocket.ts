import { useState, useEffect, useCallback } from 'react';
import { WSMessage } from '@/types';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (message: WSMessage) => void;
  reconnectAttempts?: number;
  reconnectInterval?: number;
}

export function useWebSocket({
  url,
  onMessage,
  reconnectAttempts = 5,
  reconnectInterval = 3000
}: UseWebSocketOptions) {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [attempts, setAttempts] = useState(0);
  const [lastMessage, setLastMessage] = useState<WSMessage | null>(null);
  const [readyState, setReadyState] = useState<number>(WebSocket.CONNECTING);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        setIsConnected(true);
        setError(null);
        setAttempts(0);
        setReadyState(WebSocket.OPEN);
      };

      ws.onclose = () => {
        setIsConnected(false);
        setReadyState(WebSocket.CLOSED);
        if (attempts < reconnectAttempts) {
          setTimeout(() => {
            setAttempts(prev => prev + 1);
            connect();
          }, reconnectInterval);
        }
      };

      ws.onerror = (event) => {
        setError('WebSocket connection error');
        setReadyState(WebSocket.CLOSED);
        console.error('WebSocket error:', event);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as WSMessage;
          setLastMessage(data);
          onMessage?.(data);
        } catch (err) {
          console.error('Error parsing WebSocket message:', err);
        }
      };

      setSocket(ws);
      setReadyState(ws.readyState);

      return () => {
        ws.close();
      };
    } catch (err) {
      setError('Failed to create WebSocket connection');
      setReadyState(WebSocket.CLOSED);
      console.error('WebSocket connection error:', err);
    }
  }, [url, attempts, reconnectAttempts, reconnectInterval, onMessage]);

  useEffect(() => {
    const cleanup = connect();
    return () => cleanup?.();
  }, [connect]);

  const sendMessage = useCallback((message: string | object) => {
    if (socket?.readyState === WebSocket.OPEN) {
      socket.send(typeof message === 'string' ? message : JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, [socket]);

  return {
    isConnected,
    error,
    sendMessage,
    lastMessage,
    readyState
  };
}