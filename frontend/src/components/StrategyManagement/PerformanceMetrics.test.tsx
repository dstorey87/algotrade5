import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { PerformanceMetrics } from './PerformanceMetrics';
import { TestWrapper } from '../../tests/utils/TestWrapper';

const mockStrategies = [
  {
    id: '1',
    name: 'Test Strategy 1',
    winRate: 85,
    profitFactor: 2.5,
    sharpeRatio: 1.8,
    maxDrawdown: 15,
  },
  {
    id: '2',
    name: 'Test Strategy 2',
    winRate: 75,
    profitFactor: 2.0,
    sharpeRatio: 1.5,
    maxDrawdown: 20,
  },
];

describe('PerformanceMetrics', () => {
  it('shows loading state initially', () => {
    render(
      <TestWrapper>
        <PerformanceMetrics strategies={[]} isLoading={true} />
      </TestWrapper>
    );

    expect(screen.getByTestId('performance-metrics-loading')).toBeInTheDocument();
  });

  it('displays strategy metrics correctly when data is loaded', async () => {
    render(
      <TestWrapper>
        <PerformanceMetrics strategies={mockStrategies} isLoading={false} />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText(/Test Strategy 1/i)).toBeInTheDocument();
      expect(screen.getByText(/Test Strategy 2/i)).toBeInTheDocument();
      expect(screen.getByText(/85%/)).toBeInTheDocument();
      expect(screen.getByText(/2.5/)).toBeInTheDocument();
    });
  });

  it('handles empty strategies array', () => {
    render(
      <TestWrapper>
        <PerformanceMetrics strategies={[]} isLoading={false} />
      </TestWrapper>
    );

    expect(screen.getByText(/No strategies available/i)).toBeInTheDocument();
  });
});