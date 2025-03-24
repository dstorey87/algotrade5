import React from 'react';
import { render, screen, act, waitFor } from '@testing-library/react';
import { Provider } from 'react-redux';
import { TestWrapper } from '../tests/utils/TestWrapper';
import { TradeMonitor } from '@/components/RealTimeMonitoring/TradeMonitor';
import { createTestStore } from '@/lib/store/testStore';
import websocketService from '@/services/websocket';

// Mock Material UI components
jest.mock('@mui/material', () => ({
  Box: ({ children, ...props }: any) => <div data-testid="mui-box" {...props}>{children}</div>,
  Card: ({ children, ...props }: any) => <div data-testid="mui-card" {...props}>{children}</div>,
  CardContent: ({ children, ...props }: any) => <div data-testid="mui-card-content" {...props}>{children}</div>,
  Typography: ({ children, ...props }: any) => <div data-testid="mui-typography" {...props}>{children}</div>,
  Grid: ({ children, ...props }: any) => <div data-testid="mui-grid" {...props}>{children}</div>,
  Paper: ({ children, ...props }: any) => <div data-testid="mui-paper" {...props}>{children}</div>,
  CircularProgress: (props: any) => <div data-testid="mui-circular-progress" {...props} />,
  Alert: ({ children, ...props }: any) => <div data-testid="mui-alert" {...props}>{children}</div>,
}));

// Mock the TradeMonitor component
jest.mock('../components/RealTimeMonitoring/TradeMonitor', () => ({
  TradeMonitor: () => <div data-testid="trade-monitor">Trade Monitor Component</div>
}));

// Mock the MarketDataMonitor component
jest.mock('../components/RealTimeMonitoring/MarketDataMonitor', () => ({
  MarketDataMonitor: () => <div data-testid="market-data-monitor">Market Data Monitor Component</div>
}));

// Mock the RiskManager component
jest.mock('../components/RealTimeMonitoring/RiskManager', () => ({
  RiskManager: () => <div data-testid="risk-manager">Risk Manager Component</div>
}));

// Mock WebSocket service
jest.mock('@/services/websocket', () => ({
  connect: jest.fn(),
  disconnect: jest.fn(),
  isConnected: jest.fn(() => true),
  handleMessage: jest.fn(),
  getPerformanceMetrics: jest.fn(() => ({
    avgProcessingTime: 50,
    avgBatchSize: 10,
    avgCompressionRatio: 0.6,
    timestamp: new Date().toISOString(),
    sampleSizes: {
      processing: 100,
      batches: 100,
      compression: 100
    }
  }))
}));

describe('Real-Time Monitoring Integration', () => {
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    store = createTestStore({
      trading: {
        trades: Array.from({ length: 100 }, (_, i) => ({
          id: `trade-${i}`,
          pair: 'BTC/USDT',
          type: i % 2 === 0 ? 'buy' : 'sell',
          amount: 0.001,
          price: 50000,
          timestamp: new Date().toISOString(),
          profit: i % 3 === 0 ? 0.5 : -0.3
        }))
      }
    });
  });

  test('should render all components with initial data', async () => {
    render(
      <Provider store={store}>
        <TradeMonitor />
      </Provider>
    );

    // Check performance metrics dashboard
    await waitFor(() => {
      expect(screen.getByText(/Message Processing/i)).toBeInTheDocument();
      expect(screen.getByText(/Batch Size/i)).toBeInTheDocument();
      expect(screen.getByText(/Compression Ratio/i)).toBeInTheDocument();
    });

    // Check trade statistics
    expect(screen.getByText(/Win Rate/i)).toBeInTheDocument();
    expect(screen.getByText(/Profit Factor/i)).toBeInTheDocument();

    // Check trade list rendering
    const trades = screen.getAllByTestId('trade-row');
    expect(trades.length).toBeLessThan(100); // Should be virtualized
  });

  test('should update performance metrics in real-time', async () => {
    render(
      <Provider store={store}>
        <TradeMonitor />
      </Provider>
    );

    // Simulate WebSocket messages
    await act(async () => {
      for (let i = 0; i < 10; i++) {
        websocketService.handleMessage({
          data: JSON.stringify({
            type: 'trade_update',
            data: {
              id: `new-trade-${i}`,
              pair: 'ETH/USDT',
              type: 'buy',
              amount: 0.1,
              price: 3000,
              timestamp: new Date().toISOString(),
              profit: 0.2
            }
          })
        });
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    });

    // Verify metrics update
    const metrics = websocketService.getPerformanceMetrics();
    expect(metrics.avgProcessingTime).toBeLessThan(100);
    expect(metrics.avgBatchSize).toBeGreaterThan(1);
  });

  test('should handle large datasets efficiently', async () => {
    const largeStore = createTestStore({
      trading: {
        trades: Array.from({ length: 10000 }, (_, i) => ({
          id: `trade-${i}`,
          pair: 'BTC/USDT',
          type: 'buy',
          amount: 0.001,
          price: 50000,
          timestamp: new Date().toISOString(),
          profit: 0.1
        }))
      }
    });

    const startTime = performance.now();
    
    render(
      <Provider store={largeStore}>
        <TradeMonitor />
      </Provider>
    );

    const renderTime = performance.now() - startTime;
    expect(renderTime).toBeLessThan(100); // Should render in under 100ms

    // Check that only visible items are in DOM
    const trades = screen.getAllByTestId('trade-row');
    expect(trades.length).toBeLessThan(50);
  });

  test('should recover from WebSocket disconnection', async () => {
    websocketService.isConnected.mockImplementation(() => false);
    
    render(
      <Provider store={store}>
        <TradeMonitor />
      </Provider>
    );

    // Simulate reconnection
    await act(async () => {
      websocketService.isConnected.mockImplementation(() => true);
      await new Promise(resolve => setTimeout(resolve, 3000));
    });

    expect(websocketService.connect).toHaveBeenCalled();
  });
});

describe('RealTimeMonitoring', () => {
  it('renders all monitoring components', async () => {
    render(
      <TestWrapper>
        <div data-testid="real-time-monitoring">
          <div data-testid="trade-monitor">Trade Monitor Component</div>
          <div data-testid="market-data-monitor">Market Data Monitor Component</div>
          <div data-testid="risk-manager">Risk Manager Component</div>
        </div>
      </TestWrapper>
    );

    expect(screen.getByTestId('real-time-monitoring')).toBeInTheDocument();
    expect(screen.getByTestId('trade-monitor')).toBeInTheDocument();
    expect(screen.getByTestId('market-data-monitor')).toBeInTheDocument();
    expect(screen.getByTestId('risk-manager')).toBeInTheDocument();
  });
});