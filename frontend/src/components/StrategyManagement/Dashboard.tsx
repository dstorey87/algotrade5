import React from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { StrategyList } from './StrategyList';
import { StrategyEditor } from './StrategyEditor';
import { PerformanceMetrics } from './PerformanceMetrics';
import { fetchStrategies, updateStrategy } from '@/lib/api/strategies';
import type { Strategy } from '@/types';

export const StrategyManagementDashboard: React.FC = () => {
    const { data: strategies, isLoading } = useQuery<Strategy[]>({
        queryKey: ['strategies'],
        queryFn: fetchStrategies
    });

    const updateMutation = useMutation({
        mutationFn: updateStrategy
    });

    return (
        <div className="grid grid-cols-12 gap-4 p-4" data-testid="strategy-management-dashboard">
            <div className="col-span-12 lg:col-span-3">
                <StrategyList 
                    strategies={strategies || []} 
                    isLoading={isLoading}
                />
            </div>
            <div className="col-span-12 lg:col-span-6">
                <StrategyEditor 
                    onSave={updateMutation.mutate}
                    isUpdating={updateMutation.isPending}
                />
            </div>
            <div className="col-span-12 lg:col-span-3">
                <PerformanceMetrics strategies={strategies || []} />
            </div>
        </div>
    );
};