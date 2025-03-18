import { AppDispatch } from '@/lib/store';
import { 
  updateActiveTrades,
  updateTradeHistory,
  updateBalance,
  updatePerformanceStats,
  setError
} from '@/lib/slices/tradingSlice';
import apiSettings from '@/config/api';

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
        this.dispatch(setError(`WebSocket connection error: ${error instanceof Error ? error.message : String(error)}`));
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

  // Handle incoming WebSocket messages
  private handleMessage(event: MessageEvent): void {
    if (!this.dispatch) return;

    try {
      const message: WSMessage = JSON.parse(event.data);
      
      switch (message.type) {
        case 'trade_update':
          // Update active trades and trade history
          if (message.data.is_open) {
            this.dispatch(updateActiveTrades(message.data.trades));
          } else {
            this.dispatch(updateTradeHistory(message.data.trades));
          }
          break;
        
        case 'balance_update':
          // Update wallet balance
          this.dispatch(updateBalance(message.data));
          break;

        case 'performance_update':
          // Update performance metrics
          this.dispatch(updatePerformanceStats(message.data));
          break;

        case 'error':
          // Handle error messages
          this.dispatch(setError(message.data.error));
          break;

        default:
          // Log other message types for debugging
          console.log(`Received message of type: ${message.type}`, message.data);
      }
    } catch (error) {
      console.error('Error parsing WebSocket message:', error);
    }
  }

  // Handle WebSocket errors
  private handleError(event: Event): void {
    this.isConnecting = false;
    console.error('WebSocket error:', event);
    if (this.dispatch) {
      this.dispatch(setError('WebSocket connection error'));
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
}

// Create singleton instance
const websocketService = new WebSocketService();
export default websocketService;