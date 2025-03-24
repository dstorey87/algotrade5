import { act, render, screen } from '@testing-library/react';
import { Provider } from 'react-redux';
import { store } from '@/lib/store';
import { TradeMonitor } from '@/components/RealTimeMonitoring/TradeMonitor';
import { VirtualizedTradeList } from '@/components/RealTimeMonitoring/VirtualizedTradeList';
import { PerformanceMetricsDashboard } from '@/components/RealTimeMonitoring/PerformanceMetricsDashboard';
import websocketService from '@/services/websocket';

describe('Component Integration Tests', () => {
  beforeEach(() => {
    // Clear performance metrics before each test
    websocketService.getPerformanceMetrics();
  });

  test('TradeMonitor renders with all sub-components', () => {
    render(
      <Provider store={store}>
        <TradeMonitor />
      </Provider>
    );

    // Check for main components
    expect(screen.getByText(/Real-time Performance Metrics/i)).toBeInTheDocument();
    expect(screen.getByText(/Win Rate:/i)).toBeInTheDocument();
    expect(screen.getByTestId('trades-panel')).toBeInTheDocument();
  });

  test('VirtualizedTradeList handles large datasets efficiently', async () => {
    const mockTrades = Array.from({ length: 1000 }, (_, i) => ({
      id: `trade-${i}`,
      pair: 'BTC/USDT',
      type: 'buy',
      amount: 0.001,
      price: 50000,
      timestamp: new Date().toISOString(),
      profit: 0
    }));

    const { container } = render(
      <Provider store={store}>
        <VirtualizedTradeList trades={mockTrades} />
      </Provider>
    );

    // Verify only a subset of DOM nodes are rendered
    const renderedItems = container.querySelectorAll('.trade-row');
    expect(renderedItems.length).toBeLessThan(mockTrades.length);
  });

  test('PerformanceMetricsDashboard updates with WebSocket metrics', async () => {
    render(
      <Provider store={store}>
        <PerformanceMetricsDashboard />
      </Provider>
    );

    // Simulate some WebSocket activity
    await act(async () => {
      for (let i = 0; i < 10; i++) {
        websocketService.handleMessage({ data: JSON.stringify({
          type: 'trade_update',
          data: { id: `test-${i}` }
        })});
        await new Promise(resolve => setTimeout(resolve, 100));
      }
    });

    // Check for metric updates
    expect(screen.getByText(/Message Processing/i)).toBeInTheDocument();
    expect(screen.getByText(/Batch Size/i)).toBeInTheDocument();
    expect(screen.getByText(/Compression Ratio/i)).toBeInTheDocument();
  });

  test('Model preloading works correctly', async () => {
    const { result } = renderHook(() => useModelLoader({
      preloadModels: ['trade_analyzer'],
      maxCacheSize: 5
    }));

    // Wait for preloading to complete
    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
    });

    const status = result.current.getModelStatus('trade_analyzer');
    expect(status.isLoaded).toBe(true);
    expect(status.isLoading).toBe(false);
  });
});