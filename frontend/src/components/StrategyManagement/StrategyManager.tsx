import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { StrategyList } from './StrategyList';
import { StrategyEditor } from './StrategyEditor';
import { PerformanceMetrics } from './PerformanceMetrics';
import { fetchStrategies, updateStrategy } from '@/lib/api/strategies';
import type { Strategy } from '@/types';

export const StrategyManager: React.FC = () => {
    const [selectedStrategyId, setSelectedStrategyId] = useState<string | null>(null);
    const { data: strategies, isLoading } = useQuery({
        queryKey: ['strategies'],
        queryFn: fetchStrategies
    });
    
    const updateMutation = useMutation({
        mutationFn: updateStrategy
    });

    const selectedStrategy = strategies?.find(s => s.id === selectedStrategyId);

    return (
        <div className="grid grid-cols-12 gap-4 p-4" data-testid="strategy-manager">
            <div className="col-span-12 lg:col-span-4">
                <StrategyList 
                    strategies={strategies || []} 
                    isLoading={isLoading}
                />
            </div>
            <div className="col-span-12 lg:col-span-8">
                <StrategyEditor 
                    onSave={updateMutation.mutate}
                    isUpdating={updateMutation.isPending}
                />
            </div>
            <div className="col-span-12 lg:col-span-12">
                <PerformanceMetrics 
                    strategies={strategies}
                    isLoading={isLoading}
                />
            </div>
        </div>
    );
};
