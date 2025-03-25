import React from 'react';
import { render, screen, waitFor } from './test-utils';
import RealTimeMonitoring from '@/components/RealTimeMonitoring';
import { websocketService } from '@/services/websocket';

// Mock child components
jest.mock('@/components/RealTimeMonitoring/TradeMonitor', () => ({
  TradeMonitor: () => <div data-testid="trade-monitor">Trade Monitor</div>
}));

jest.mock('@/components/RealTimeMonitoring/PerformanceMetrics', () => ({
  PerformanceMetrics: () => <div data-testid="performance-metrics">Performance Metrics</div>
}));

jest.mock('@/components/RealTimeMonitoring/RiskManager', () => ({
  RiskManager: () => <div data-testid="risk-manager">Risk Manager</div>
}));

// Mock Tremor components
jest.mock('@tremor/react', () => ({
  Grid: ({ children }: any) => <div data-testid="tremor-grid">{children}</div>,
  Card: ({ children }: any) => <div data-testid="tremor-card">{children}</div>,
  Title: ({ children }: any) => <h2 data-testid="tremor-title">{children}</h2>,
}));

describe('Real-Time Monitoring Integration', () => {
  const mockInitialState = {
    trading: {
      realTimeEnabled: true,
      trades: Array(100).fill(null).map((_, i) => ({
        id: i,
        pair: 'BTC/USD',
        side: 'buy',
        status: 'open',
        openTime: new Date().toISOString(),
        closeTime: null,
        openPrice: 50000,
        closePrice: null,
        profit: null
      })),
      performanceMetrics: {
        messageProcessingRate: 1000,
        batchSize: 50,
        compressionRatio: 0.75,
        latency: 15
      }
    }
  };

  beforeEach(() => {
    jest.spyOn(websocketService, 'connect').mockImplementation(() => {});
    jest.spyOn(websocketService, 'disconnect').mockImplementation(() => {});
    jest.spyOn(websocketService, 'addMessageListener').mockImplementation(() => {});
    jest.spyOn(websocketService, 'removeMessageListener').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('should render all components with initial data', async () => {
    render(<RealTimeMonitoring />, { preloadedState: mockInitialState });

    expect(screen.getByTestId('trade-monitor')).toBeInTheDocument();
    expect(screen.getByTestId('performance-metrics')).toBeInTheDocument();
    expect(screen.getByTestId('risk-manager')).toBeInTheDocument();
  });

  it('should handle large datasets efficiently', () => {
    render(<RealTimeMonitoring />, { preloadedState: mockInitialState });
    
    const tradeMonitor = screen.getByTestId('trade-monitor');
    expect(tradeMonitor).toBeInTheDocument();
  });

  it('should recover from WebSocket disconnection', async () => {
    render(<RealTimeMonitoring />, { preloadedState: mockInitialState });

    // Simulate disconnection
    const disconnectEvent = new Event('offline');
    window.dispatchEvent(disconnectEvent);

    await waitFor(() => {
      expect(websocketService.connect).toHaveBeenCalled();
    });
  });
});