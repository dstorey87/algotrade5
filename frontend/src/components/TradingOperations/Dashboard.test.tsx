import React from 'react';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { TradingOperationsDashboard } from './Dashboard';

const queryClient = new QueryClient();

describe('TradingOperationsDashboard', () => {
    beforeEach(() => {
        render(
            <QueryClientProvider client={queryClient}>
                <TradingOperationsDashboard />
            </QueryClientProvider>
        );
    });

    it('renders trade monitor component', () => {
        expect(screen.getByTestId('trade-monitor')).toBeInTheDocument();
    });

    it('renders strategy control component', () => {
        expect(screen.getByTestId('strategy-control')).toBeInTheDocument();
    });

    it('renders performance metrics component', () => {
        expect(screen.getByTestId('performance-metrics')).toBeInTheDocument();
    });
});
