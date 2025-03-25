import React from 'react';
import { render, screen, waitFor } from '@/tests/test-utils';
import { PerformanceMetrics } from './PerformanceMetrics';

// Mock Tremor components
jest.mock('@tremor/react', () => ({
  Card: ({ children }: any) => <div data-testid="tremor-card">{children}</div>,
  Grid: ({ children, numItems, numItemsMd }: any) => (
    <div data-testid="tremor-grid" data-items={numItems} data-items-md={numItemsMd}>
      {children}
    </div>
  ),
  Title: ({ children }: any) => <h3 className="font-medium mb-2">{children}</h3>,
  Metric: ({ children }: any) => <p className="text-lg font-semibold">{children}</p>,
}));

describe('PerformanceMetrics', () => {
  const mockPerformanceData = {
    messageProcessingRate: 1000,
    batchSize: 50,
    compressionRatio: 0.75,
    latency: 15
  };

  it('displays strategy metrics correctly when data is loaded', async () => {
    render(<PerformanceMetrics {...mockPerformanceData} />);

    await waitFor(() => {
      expect(screen.getByText('Message Processing Rate')).toBeInTheDocument();
      expect(screen.getByText('1000/s')).toBeInTheDocument();
      expect(screen.getByText('50')).toBeInTheDocument();
      expect(screen.getByText('75.0%')).toBeInTheDocument();
      expect(screen.getByText('15ms')).toBeInTheDocument();
    });
  });

  it('shows default values when no data is provided', () => {
    render(<PerformanceMetrics />);

    expect(screen.getByText('0/s')).toBeInTheDocument();
    expect(screen.getByText('0')).toBeInTheDocument();
    expect(screen.getByText('0.0%')).toBeInTheDocument();
    expect(screen.getByText('0ms')).toBeInTheDocument();
  });
});