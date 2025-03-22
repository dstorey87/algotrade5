import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { TradeMonitor } from '../TradingControls/TradeMonitor';
import { StrategyManager } from '../StrategyManagement/StrategyManager';
import { PerformanceMetrics } from '../StrategyManagement/PerformanceMetrics';

export const TradingOperationsDashboard: React.FC = () => {
    const { data: systemStatus } = useQuery({ 
        queryKey: ['systemStatus'], 
        queryFn: () => fetch('/api/system/status').then(res => res.json())
    });

    return (
        <div className="grid grid-cols-12 gap-4 p-4">
            <div className="col-span-12 lg:col-span-8" data-testid="trade-monitor">
                <TradeMonitor />
            </div>
            <div className="col-span-12 lg:col-span-4" data-testid="strategy-control">
                <StrategyManager />
            </div>
            <div className="col-span-12" data-testid="performance-metrics">
                <PerformanceMetrics />
            </div>
        </div>
    );
};