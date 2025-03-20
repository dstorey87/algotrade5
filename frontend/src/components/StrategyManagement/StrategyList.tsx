import React from 'react';
import { Strategy } from '@/types';

interface StrategyListProps {
    strategies: Strategy[];
    isLoading: boolean;
}

export const StrategyList: React.FC<StrategyListProps> = ({ strategies, isLoading }) => {
    if (isLoading) {
        return (
            <div className="p-4 bg-white rounded-lg shadow" data-testid="strategy-list-loading">
                <div className="animate-pulse space-y-4">
                    {[1, 2, 3].map((i) => (
                        <div key={i} className="h-12 bg-gray-200 rounded"></div>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg shadow" data-testid="strategy-list">
            <div className="p-4 border-b">
                <h2 className="text-lg font-semibold">Trading Strategies</h2>
            </div>
            <div className="divide-y">
                {strategies.map((strategy) => (
                    <div
                        key={strategy.id}
                        className="p-4 hover:bg-gray-50 cursor-pointer transition-colors"
                        data-testid={`strategy-item-${strategy.id}`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <h3 className="font-medium">{strategy.name}</h3>
                                <p className="text-sm text-gray-500">Win Rate: {(strategy.performance.winRate * 100).toFixed(1)}%</p>
                            </div>
                            <div className={`px-2 py-1 rounded text-sm ${
                                strategy.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                            }`}>
                                {strategy.isActive ? 'Active' : 'Inactive'}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};