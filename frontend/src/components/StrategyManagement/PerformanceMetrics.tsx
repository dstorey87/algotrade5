import React from 'react';
import { useQuery } from 'react-query';
import { Strategy } from '@/types';
import { fetchStrategyPerformance } from '@/lib/api/strategies';

interface PerformanceMetricsProps {
    strategies: Strategy[];
}

export const PerformanceMetrics: React.FC<PerformanceMetricsProps> = ({ strategies }) => {
    const { data: performance, isLoading } = useQuery(
        ['strategyPerformance', strategies.map(s => s.id)],
        () => Promise.all(strategies.map(s => fetchStrategyPerformance(s.id)))
    );

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