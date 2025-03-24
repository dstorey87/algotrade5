import { AppDispatch } from '@/lib/store';
import {
  updateSystemStatus,
  updateBalance,
  updateTrades,
  updatePerformanceStats,
  resetError
} from '@/store/slices/tradingSlice';
import apiSettings from '@/config/api';
import msgpack from 'msgpack-lite';

// WebSocket message types
type WSMessageType = 
  | 'trade_update'
  | 'balance_update'
  | 'performance_update'
  | 'status'
  | 'whitelist'
  | 'blacklist'
  | 'analyzed_df'
  | 'error';

interface WSMessage {
  type: WSMessageType;
  data: any;
}

class WebSocketService {
  private socket: WebSocket | null = null;
  private dispatch: AppDispatch | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 2000; // Base delay in ms
  private isConnecting = false;
  private messageBuffer: Array<WSMessage> = [];
  private batchTimeout: ReturnType<typeof setTimeout> | null = null;
  private readonly BATCH_INTERVAL = 100; // 100ms batching window
  private readonly MAX_BATCH_SIZE = 100; // Maximum messages per batch
  private readonly messageCache = new Map<string, {data: any, timestamp: number}>();
  private readonly CACHE_TTL = 60000; // 1 minute cache TTL
  private readonly metrics = {
    messageProcessingTimes: [] as number[],
    batchSizes: [] as number[],
    compressionRatios: [] as number[]
  };

  // Initialize WebSocket connection
  public connect(dispatch: AppDispatch): void {
    if (this.socket?.readyState === WebSocket.OPEN || this.isConnecting) {
      return;
    }

    this.dispatch = dispatch;
    this.isConnecting = true;

    const token = apiSettings.getToken();
    const wsUrl = apiSettings.wsUrl(`trades?token=${token}`);

    try {
      // Connect to the FreqTrade WebSocket API
      this.socket = new WebSocket(wsUrl);

      this.socket.onopen = this.handleOpen.bind(this);
      this.socket.onmessage = this.handleMessage.bind(this);
      this.socket.onerror = this.handleError.bind(this);
      this.socket.onclose = this.handleClose.bind(this);
    } catch (error) {
      this.isConnecting = false;
      if (this.dispatch) {
        this.dispatch(resetError());
        console.error(`WebSocket connection error: ${error instanceof Error ? error.message : String(error)}`);
      }
      this.attemptReconnect();
    }
  }

  // Handle WebSocket open event
  private handleOpen(): void {
    this.isConnecting = false;
    this.reconnectAttempts = 0;
    console.log('WebSocket connection established');
  }

  private compressMessage(data: any): Uint8Array {
    return msgpack.encode(data);
  }

  private decompressMessage(data: ArrayBuffer): any {
    return msgpack.decode(new Uint8Array(data));
  }

  private logMetrics(type: keyof typeof this.metrics, value: number) {
    this.metrics[type].push(value);
    if (this.metrics[type].length > 100) {
      this.metrics[type].shift();
    }
  }

  // Handle incoming WebSocket messages
  private handleMessage(event: MessageEvent): void {
    if (!this.dispatch) return;

    const startTime = performance.now();
    try {
      const originalSize = event.data.byteLength;
      const message: WSMessage = this.decompressMessage(event.data);
      const decompressedSize = JSON.stringify(message).length;
      
      this.logMetrics('compressionRatios', originalSize / decompressedSize);
      
      // Check cache for duplicate messages
      const cacheKey = `${message.type}-${JSON.stringify(message.data)}`;
      const cachedMessage = this.messageCache.get(cacheKey);
      if (cachedMessage && Date.now() - cachedMessage.timestamp < this.CACHE_TTL) {
        return; // Skip duplicate message still in cache
      }
      
      // Update cache with compressed data
      this.messageCache.set(cacheKey, {
        data: this.compressMessage(message.data),
        timestamp: Date.now()
      });

      // Add to batch buffer
      this.messageBuffer.push(message);
      
      // Adaptive batch size based on message frequency
      const batchSize = this.calculateOptimalBatchSize();
      
      if (!this.batchTimeout && this.messageBuffer.length < batchSize) {
        this.batchTimeout = setTimeout(() => this.processBatch(), this.BATCH_INTERVAL);
      } else if (this.messageBuffer.length >= batchSize) {
        if (this.batchTimeout) {
          clearTimeout(this.batchTimeout);
          this.batchTimeout = null;
        }
        this.processBatch();
      }

      this.logMetrics('messageProcessingTimes', performance.now() - startTime);
    } catch (error) {
      console.error('Error processing WebSocket message:', error);
    }
  }

  // Calculate optimal batch size based on message frequency
  private calculateOptimalBatchSize(): number {
    const messageRate = this.messageBuffer.length / (this.BATCH_INTERVAL / 1000);
    // Adjust batch size based on message rate, with min/max bounds
    return Math.max(10, Math.min(this.MAX_BATCH_SIZE, Math.ceil(messageRate * 1.5)));
  }

  private processBatch(): void {
    if (!this.messageBuffer.length || !this.dispatch) return;

    const startTime = performance.now();
    // Group messages by type
    const batchedUpdates = this.messageBuffer.reduce((acc, message) => {
      if (!acc[message.type]) {
        acc[message.type] = [];
      }
      acc[message.type].push(message.data);
      return acc;
    }, {} as Record<string, any[]>);

    // Dispatch batched updates
    Object.entries(batchedUpdates).forEach(([type, data]) => {
      switch (type as WSMessageType) {
        case 'trade_update':
          this.dispatch!(updateTrades(data));
          break;
        case 'balance_update':
          this.dispatch!(updateBalance(data[data.length - 1])); // Use latest balance
          break;
        case 'performance_update':
          this.dispatch!(updatePerformanceStats(data[data.length - 1])); // Use latest stats
          break;
        case 'error':
          console.error('WebSocket errors:', data);
          this.dispatch!(resetError());
          break;
        default:
          console.log(`Batch processed for type: ${type}`, data);
      }
    });

    this.logMetrics('batchSizes', this.messageBuffer.length);
    this.logMetrics('messageProcessingTimes', performance.now() - startTime);

    // Clear batch
    this.messageBuffer = [];
    this.batchTimeout = null;

    // Clean old cache entries
    this.cleanCache();
  }

  private cleanCache(): void {
    const now = Date.now();
    // Fix iteration approach to work with lower TypeScript targets
    Array.from(this.messageCache.entries()).forEach(([key, value]) => {
      if (now - value.timestamp > this.CACHE_TTL) {
        this.messageCache.delete(key);
      }
    });
  }

  // Handle WebSocket errors
  private handleError(event: Event): void {
    this.isConnecting = false;
    console.error('WebSocket error:', event);
    if (this.dispatch) {
      this.dispatch(resetError());
    }
  }

  // Handle WebSocket connection close
  private handleClose(event: CloseEvent): void {
    this.isConnecting = false;
    console.log(`WebSocket connection closed: ${event.code} ${event.reason}`);
    this.attemptReconnect();
  }

  // Attempt to reconnect with exponential backoff
  private attemptReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts || this.isConnecting) {
      return;
    }

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    // Exponential backoff for reconnect attempts
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts);
    
    this.reconnectTimer = setTimeout(() => {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      
      if (this.dispatch) {
        // Re-establish connection with the same dispatch
        this.connect(this.dispatch);
      }
    }, delay);
  }

  // Disconnect WebSocket
  public disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }

    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }

  // Check if WebSocket is connected
  public isConnected(): boolean {
    return this.socket !== null && this.socket.readyState === WebSocket.OPEN;
  }

  // Add method to get performance metrics
  public getPerformanceMetrics() {
    const avg = (arr: number[]) => arr.reduce((a, b) => a + b, 0) / arr.length;
    
    return {
      avgProcessingTime: avg(this.metrics.messageProcessingTimes),
      avgBatchSize: avg(this.metrics.batchSizes),
      avgCompressionRatio: avg(this.metrics.compressionRatios),
      timestamp: new Date().toISOString(),
      sampleSizes: {
        processing: this.metrics.messageProcessingTimes.length,
        batches: this.metrics.batchSizes.length,
        compression: this.metrics.compressionRatios.length
      }
    };
  }
}

// Create singleton instance
const websocketService = new WebSocketService();
export default websocketService;