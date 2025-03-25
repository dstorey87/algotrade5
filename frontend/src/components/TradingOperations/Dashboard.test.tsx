import React from 'react';
import { render, screen } from '@/tests/test-utils';
import Dashboard from './index';

// Mock child components
jest.mock('@/components/StrategyControl', () => ({
  StrategyControl: () => <div data-testid="strategy-control">Strategy Control</div>
}));

jest.mock('@/components/PerformanceMetrics', () => ({
  PerformanceMetrics: () => <div data-testid="performance-metrics">Performance Metrics</div>
}));

// Mock Tremor components
jest.mock('@tremor/react', () => ({
  Grid: ({ children }: any) => <div data-testid="tremor-grid">{children}</div>,
  Card: ({ children }: any) => <div data-testid="tremor-card">{children}</div>,
  Title: ({ children }: any) => <h2 data-testid="tremor-title">{children}</h2>
}));

describe('Dashboard', () => {
  const mockInitialState = {
    trading: {
      currentStrategy: {
        id: '1',
        name: 'Test Strategy',
        performance: {
          winRate: 0.75,
          profitFactor: 1.5,
          totalTrades: 100,
          averageProfit: 2.5
        }
      },
      balance: {
        total: 1000,
        free: 800,
        used: 200
      },
      performanceStats: {
        wins: 75,
        losses: 25,
        totalProfit: 250,
        totalLoss: -50,
        trades: 100
      }
    }
  };

  it('renders strategy control component', () => {
    render(<Dashboard />, { preloadedState: mockInitialState });
    expect(screen.getByTestId('strategy-control')).toBeInTheDocument();
  });

  it('renders performance metrics component', () => {
    render(<Dashboard />, { preloadedState: mockInitialState });
    expect(screen.getByTestId('performance-metrics')).toBeInTheDocument();
  });
});
