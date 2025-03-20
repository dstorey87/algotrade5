import { Strategy } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface StrategyUpdate {
  id: string;
  name?: string;
  code?: string;
  parameters?: Record<string, any>;
  isActive?: boolean;
}

export interface StrategyPerformance {
  winRate: number;
  profitFactor: number;
  totalTrades: number;
  averageProfit: number;
  drawdown: number;
}

export async function fetchStrategies(): Promise<Strategy[]> {
  const response = await fetch(`${API_BASE_URL}/api/strategies`);
  if (!response.ok) {
    throw new Error('Failed to fetch strategies');
  }
  return response.json();
}

export async function updateStrategy(update: StrategyUpdate): Promise<Strategy> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/${update.id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(update),
  });
  if (!response.ok) {
    throw new Error('Failed to update strategy');
  }
  return response.json();
}

export async function fetchStrategyPerformance(strategyId: string): Promise<StrategyPerformance> {
  const response = await fetch(`${API_BASE_URL}/api/strategies/${strategyId}/performance`);
  if (!response.ok) {
    throw new Error('Failed to fetch strategy performance');
  }
  return response.json();
}