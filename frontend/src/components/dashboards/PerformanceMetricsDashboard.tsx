import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { tradingService } from '@/services/tradingService';

interface TradeMetrics {
  winRate: number;
  profitFactor: number;
  totalTrades: number;
  avgProfit: number;
  maxDrawdown: number;
  profitTotal: number;
  avgDuration: string;
}

export const PerformanceMetricsDashboard = () => {
    const { data: trades, isLoading: isLoadingTrades } = useQuery({
        queryKey: ['trades'],
        queryFn: () => tradingService.getTrades()
    });

    const { data: status, isLoading: isLoadingStatus } = useQuery({
        queryKey: ['status'],
        queryFn: () => tradingService.getTradingStatus()
    });

    const calculateMetrics = (trades: any[]): TradeMetrics => {
        const winningTrades = trades.filter(t => t.close_profit > 0);
        const totalProfit = trades.reduce((sum, t) => sum + t.close_profit, 0);
        const avgProfit = totalProfit / trades.length || 0;
        
        return {
            winRate: (winningTrades.length / trades.length) * 100 || 0,
            profitFactor: Math.abs(totalProfit / trades.length) || 0,
            totalTrades: trades.length,
            avgProfit: avgProfit,
            maxDrawdown: status?.max_drawdown || 0,
            profitTotal: totalProfit,
            avgDuration: status?.avg_duration || '0:00:00'
        };
    };

    const isLoading = isLoadingTrades || isLoadingStatus;
    const metrics = trades ? calculateMetrics(trades) : null;

    if (isLoading) {
        return (
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
                <div className="animate-pulse space-y-4">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
                    <div className="space-y-3">
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Performance Metrics</h2>
            </div>
            <div className="p-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Win Rate</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {metrics?.winRate.toFixed(1)}%
                    </p>
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Total Trades</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {metrics?.totalTrades}
                    </p>
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Average Profit</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {metrics?.avgProfit.toFixed(2)}%
                    </p>
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Max Drawdown</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {metrics?.maxDrawdown.toFixed(2)}%
                    </p>
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Total Profit</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {metrics?.profitTotal.toFixed(2)}%
                    </p>
                </div>
                <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">Average Duration</p>
                    <p className="text-lg font-semibold text-gray-900 dark:text-white">
                        {metrics?.avgDuration}
                    </p>
                </div>
            </div>
        </div>
    );
};
