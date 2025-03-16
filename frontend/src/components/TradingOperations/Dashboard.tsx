import React from 'react';
import { useQuery } from 'react-query';
import { TradeMonitor } from './TradeMonitor';
import { StrategyControl } from './StrategyControl';
import { PerformanceMetrics } from './PerformanceMetrics';

export const TradingOperationsDashboard: React.FC = () => {
    const { data: systemStatus } = useQuery('systemStatus', fetchSystemStatus);
    const { data: activeStrategies } = useQuery('strategies', fetchStrategies);

    return (
        <div className="grid grid-cols-12 gap-4 p-4">
            <div className="col-span-12 lg:col-span-8">
                <TradeMonitor />
            </div>
            <div className="col-span-12 lg:col-span-4">
                <StrategyControl strategies={activeStrategies} />
            </div>
            <div className="col-span-12">
                <PerformanceMetrics />
            </div>
        </div>
    );
};