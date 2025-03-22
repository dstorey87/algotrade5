import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { healthService } from '@/services/healthService';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

interface ComponentStatus {
    name: string;
    status: 'healthy' | 'warning' | 'error';
}

interface SystemStatus {
    status: 'healthy' | 'warning' | 'error';
    lastChecked: string;
    components: ComponentStatus[];
}

interface ResourceUsage {
    cpu: number;
    memory: number;
    disk: number;
    network: {
        in: number;
        out: number;
    };
}

export const SystemHealthDashboard = () => {
    const { data: healthStatus, isLoading: isLoadingHealth } = useQuery({
        queryKey: ['health'],
        queryFn: () => healthService.getHealthStatus()
    });

    const { data: resourceUsage, isLoading: isLoadingResources } = useQuery({
        queryKey: ['resources'],
        queryFn: () => healthService.getResourceUsage()
    });

    const isLoading = isLoadingHealth || isLoadingResources;

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

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'healthy':
                return 'text-green-500';
            case 'warning':
                return 'text-yellow-500';
            case 'error':
                return 'text-red-500';
            default:
                return 'text-gray-500';
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">System Health</h2>
            </div>
            <div className="p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <h3 className="text-md font-medium text-gray-900 dark:text-white mb-2">Component Status</h3>
                    <div className="space-y-2">
                        {healthStatus?.components?.map((component: ComponentStatus, index: number) => (
                            <div key={index} className="flex items-center justify-between">
                                <span className="text-sm text-gray-600 dark:text-gray-400">{component.name}</span>
                                <span className={`text-sm font-medium ${getStatusColor(component.status)}`}>
                                    {component.status}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
                <div>
                    <h3 className="text-md font-medium text-gray-900 dark:text-white mb-2">Resource Usage</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="w-24 h-24">
                            <CircularProgressbar
                                value={resourceUsage?.cpu || 0}
                                text={`${resourceUsage?.cpu || 0}%`}
                                styles={{
                                    path: { stroke: '#10B981' },
                                    text: { fill: '#10B981', fontSize: '16px' }
                                }}
                            />
                            <p className="text-sm text-center mt-2 text-gray-600 dark:text-gray-400">CPU</p>
                        </div>
                        <div className="w-24 h-24">
                            <CircularProgressbar
                                value={resourceUsage?.memory || 0}
                                text={`${resourceUsage?.memory || 0}%`}
                                styles={{
                                    path: { stroke: '#3B82F6' },
                                    text: { fill: '#3B82F6', fontSize: '16px' }
                                }}
                            />
                            <p className="text-sm text-center mt-2 text-gray-600 dark:text-gray-400">Memory</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
