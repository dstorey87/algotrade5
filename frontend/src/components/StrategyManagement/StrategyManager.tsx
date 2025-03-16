import React from 'react';
import { useQuery, useMutation } from 'react-query';
import { StrategyList } from './StrategyList';
import { StrategyEditor } from './StrategyEditor';
import { PerformanceMetrics } from './PerformanceMetrics';

export const StrategyManager: React.FC = () => {
    const { data: strategies } = useQuery('strategies', fetchStrategies);
    const { mutate: updateStrategy } = useMutation(updateStrategyConfig);

    return (
        <div className="grid grid-cols-12 gap-4 p-4" data-testid="strategy-manager">
            <div className="col-span-12 lg:col-span-4">
                <StrategyList strategies={strategies} onSelect={handleStrategySelect} />
            </div>
            <div className="col-span-12 lg:col-span-8">
                <StrategyEditor strategy={selectedStrategy} onSave={updateStrategy} />
                <PerformanceMetrics strategyId={selectedStrategy?.id} />
            </div>
        </div>
    );
};
