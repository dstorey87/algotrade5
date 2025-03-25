import { io, Socket } from 'socket.io-client';
import * as msgpack from 'msgpack-lite';

export interface Trade {
  id: string;
  pair: string;
  type: 'buy' | 'sell';
  profit: number;
  timestamp: string;
}

export interface PerformanceMetrics {
  messageProcessingRate: number;
  batchSize: number;
  compressionRatio: number;
  latency: number;
}

export interface WebSocketData {
  trades: Trade[];
  metrics: PerformanceMetrics;
}

export class WebSocketService {
  private socket: Socket | null = null;
  private messageQueue: WebSocketData[] = [];
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectInterval = 1000;
  private batchSize = 100;
  private processingInterval = 100; // ms
  private batchTimeout: NodeJS.Timeout | null = null;
  private messageCount = 0;
  private lastProcessTime = Date.now();
  private listeners: ((data: WebSocketData) => void)[] = [];
  private connectionListeners: ((connected: boolean) => void)[] = [];

  private performanceMetrics: PerformanceMetrics = {
    messageProcessingRate: 0,
    batchSize: 0,
    compressionRatio: 0,
    latency: 0
  };

  constructor(private url: string = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000') {}

  public connect() {
    try {
      this.socket = io(this.url, {
        transports: ['websocket'],
        reconnection: false, // We handle reconnection manually
        timeout: 10000
      });

      this.setupEventHandlers();
      this.startMessageProcessing();
      return this.socket;
    } catch (error) {
      console.error('WebSocket connection error:', error);
      this.attemptReconnect();
      return null;
    }
  }

  private setupEventHandlers() {
    if (!this.socket) return;

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.reconnectInterval = 1000;
      this.notifyConnectionListeners(true);
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
      this.notifyConnectionListeners(false);
      this.attemptReconnect();
    });

    this.socket.on('trade_data', (data: Uint8Array) => {
      try {
        const startTime = performance.now();
        const decodedData = msgpack.decode(data) as WebSocketData;
        const processingTime = performance.now() - startTime;
        
        // Calculate compression ratio
        const jsonSize = new TextEncoder().encode(JSON.stringify(decodedData)).length;
        const compressedSize = data.byteLength;
        const compressionRatio = jsonSize / compressedSize;

        this.messageCount++;
        this.messageQueue.push(decodedData);

        // Update performance metrics
        this.performanceMetrics = {
          messageProcessingRate: this.calculateMessageRate(),
          batchSize: this.messageQueue.length,
          compressionRatio,
          latency: processingTime
        };
      } catch (error) {
        console.error('Error processing message:', error);
      }
    });

    this.socket.on('error', (error: Error) => {
      console.error('WebSocket error:', error);
      this.attemptReconnect();
    });
  }

  private calculateMessageRate(): number {
    const now = Date.now();
    const elapsed = (now - this.lastProcessTime) / 1000; // Convert to seconds
    const rate = this.messageCount / elapsed;
    
    // Reset counters every second
    if (elapsed >= 1) {
      this.messageCount = 0;
      this.lastProcessTime = now;
    }
    
    return rate;
  }

  private startMessageProcessing() {
    setInterval(() => {
      if (this.messageQueue.length === 0) return;

      const batch = this.messageQueue.splice(0, this.batchSize);
      const mergedData: WebSocketData = {
        trades: [],
        metrics: this.performanceMetrics
      };

      batch.forEach(data => {
        if (data.trades) {
          mergedData.trades.push(...data.trades);
        }
      });

      // Compress the merged data before sending
      const compressed = msgpack.encode(mergedData);
      this.notifyListeners(mergedData);
      
      if (this.socket?.connected) {
        this.socket.emit('processed_data', compressed);
      }
    }, this.processingInterval);
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Maximum reconnection attempts reached');
      return;
    }

    setTimeout(() => {
      console.log(`Attempting to reconnect (${this.reconnectAttempts + 1}/${this.maxReconnectAttempts})`);
      this.reconnectAttempts++;
      this.connect();
      // Exponential backoff
      this.reconnectInterval = Math.min(this.reconnectInterval * 2, 30000);
    }, this.reconnectInterval);
  }

  public addListener(callback: (data: WebSocketData) => void) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(cb => cb !== callback);
    };
  }

  public addConnectionListener(callback: (connected: boolean) => void) {
    this.connectionListeners.push(callback);
    return () => {
      this.connectionListeners = this.connectionListeners.filter(cb => cb !== callback);
    };
  }

  private notifyListeners(data: WebSocketData) {
    this.listeners.forEach(callback => callback(data));
  }

  private notifyConnectionListeners(connected: boolean) {
    this.connectionListeners.forEach(callback => callback(connected));
  }

  public disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
    if (this.batchTimeout) {
      clearTimeout(this.batchTimeout);
    }
    this.messageQueue = [];
    this.listeners = [];
    this.connectionListeners = [];
  }

  public isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

// Create a singleton instance
const websocketService = new WebSocketService();
export default websocketService;