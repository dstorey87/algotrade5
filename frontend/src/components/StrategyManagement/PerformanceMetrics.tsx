import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Strategy } from '@/types';
import { fetchStrategies, fetchStrategyPerformance } from '@/lib/api/strategies';

interface PerformanceMetricsProps {
    strategies?: Strategy[];
    isLoading?: boolean;
}

export const PerformanceMetrics: React.FC<PerformanceMetricsProps> = ({ 
    strategies: propStrategies, 
    isLoading: propIsLoading 
}) => {
    const { data: fetchedStrategies, isLoading: isLoadingStrategies } = useQuery({
        queryKey: ['strategies'],
        queryFn: fetchStrategies,
        enabled: propStrategies === undefined, // Only fetch if strategies prop is not provided
    });

    const strategies = propStrategies || fetchedStrategies;
    
    const { data: performance, isLoading: isLoadingPerformance } = useQuery({
        queryKey: ['strategyPerformance', strategies?.map(s => s.id)],
        queryFn: () => Promise.all((strategies || []).map(s => fetchStrategyPerformance(s.id))),
        enabled: !!strategies && propIsLoading !== true,
    });

    const isLoading = propIsLoading !== undefined ? propIsLoading : (isLoadingStrategies || isLoadingPerformance);

    if (isLoading) {
        return (
            <div className="bg-white rounded-lg shadow p-4" data-testid="performance-metrics-loading">
                <div className="animate-pulse space-y-4">
                    <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                    <div className="space-y-3">
                        <div className="h-4 bg-gray-200 rounded"></div>
                        <div className="h-4 bg-gray-200 rounded"></div>
                        <div className="h-4 bg-gray-200 rounded"></div>
                    </div>
                </div>
            </div>
        );
    }

    if (!strategies || strategies.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow" data-testid="performance-metrics">
                <div className="p-4 border-b">
                    <h2 className="text-lg font-semibold">Performance Metrics</h2>
                </div>
                <div className="p-4">
                    <p className="text-gray-500">No strategies available</p>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow" data-testid="performance-metrics">
            <div className="p-4 border-b">
                <h2 className="text-lg font-semibold">Performance Metrics</h2>
            </div>
            <div className="p-4 space-y-4">
                {performance?.map((perf, index) => (
                    <div key={strategies[index].id} className="border-b pb-4 last:border-0">
                        <h3 className="font-medium mb-2">{strategies[index].name}</h3>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-gray-500">Win Rate</p>
                                <p className="text-lg font-semibold">
                                    {(perf.winRate * 100).toFixed(1)}%
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Profit Factor</p>
                                <p className="text-lg font-semibold">
                                    {perf.profitFactor.toFixed(2)}
                                </p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Total Trades</p>
                                <p className="text-lg font-semibold">{perf.totalTrades}</p>
                            </div>
                            <div>
                                <p className="text-sm text-gray-500">Avg Profit</p>
                                <p className="text-lg font-semibold">
                                    £{perf.averageProfit.toFixed(2)}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};