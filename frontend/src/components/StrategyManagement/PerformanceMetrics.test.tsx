import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { PerformanceMetrics } from './PerformanceMetrics';

const mockStrategies = [
    {
        id: '1',
        name: 'Test Strategy 1',
        winRate: 0.75,
        isActive: true
    },
    {
        id: '2',
        name: 'Test Strategy 2',
        winRate: 0.65,
        isActive: false
    }
];

const mockPerformanceData = [
    {
        winRate: 0.75,
        profitFactor: 2.5,
        totalTrades: 100,
        averageProfit: 15.5
    },
    {
        winRate: 0.65,
        profitFactor: 1.8,
        totalTrades: 80,
        averageProfit: 12.3
    }
];

// Mock the API call
jest.mock('@/lib/api/strategies', () => ({
    fetchStrategyPerformance: jest.fn((id) => {
        return Promise.resolve(mockPerformanceData[parseInt(id) - 1]);
    })
}));

describe('PerformanceMetrics', () => {
    const queryClient = new QueryClient();

    beforeEach(() => {
        render(
            <QueryClientProvider client={queryClient}>
                <PerformanceMetrics strategies={mockStrategies} />
            </QueryClientProvider>
        );
    });

    it('renders loading state initially', () => {
        expect(screen.getByTestId('performance-metrics-loading')).toBeInTheDocument();
    });

    it('renders performance metrics after loading', async () => {
        const metricsContainer = await screen.findByTestId('performance-metrics');
        expect(metricsContainer).toBeInTheDocument();
        
        // Check if strategy names are displayed
        expect(screen.getByText('Test Strategy 1')).toBeInTheDocument();
        expect(screen.getByText('Test Strategy 2')).toBeInTheDocument();
        
        // Check if performance metrics are displayed
        expect(screen.getByText('75.0%')).toBeInTheDocument(); // Win rate for strategy 1
        expect(screen.getByText('2.50')).toBeInTheDocument(); // Profit factor for strategy 1
        expect(screen.getByText('100')).toBeInTheDocument(); // Total trades for strategy 1
        expect(screen.getByText('£15.50')).toBeInTheDocument(); // Avg profit for strategy 1
    });

    it('displays all performance metrics for each strategy', async () => {
        await screen.findByTestId('performance-metrics');
        
        // Strategy 1 metrics
        expect(screen.getByText('75.0%')).toBeInTheDocument();
        expect(screen.getByText('2.50')).toBeInTheDocument();
        expect(screen.getByText('100')).toBeInTheDocument();
        expect(screen.getByText('£15.50')).toBeInTheDocument();
        
        // Strategy 2 metrics
        expect(screen.getByText('65.0%')).toBeInTheDocument();
        expect(screen.getByText('1.80')).toBeInTheDocument();
        expect(screen.getByText('80')).toBeInTheDocument();
        expect(screen.getByText('£12.30')).toBeInTheDocument();
    });
});