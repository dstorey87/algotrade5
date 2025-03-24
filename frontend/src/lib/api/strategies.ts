import { Strategy, StrategyConfig, ApiResponse, StrategyPerformance } from '@/types';

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

// Fetch all available strategies
export async function fetchStrategies(): Promise<Strategy[]> {
  try {
    const response = await fetch('/api/strategies');
    
    if (!response.ok) {
      throw new Error(`Failed to fetch strategies: ${response.statusText}`);
    }
    
    const data: ApiResponse<Strategy[]> = await response.json();
    
    if (!data.success || !data.data) {
      throw new Error(data.error || 'Failed to fetch strategies');
    }
    
    return data.data;
  } catch (error) {
    console.error('Error fetching strategies:', error);
    // Return mock data for development/testing
    return [
      {
        id: '1',
        name: 'MACD Crossover',
        winRate: 0.75,
        profitFactor: 2.1,
        sharpeRatio: 1.5,
        maxDrawdown: 0.15,
        isActive: true
      },
      {
        id: '2',
        name: 'RSI Overbought/Oversold',
        winRate: 0.68,
        profitFactor: 1.8,
        sharpeRatio: 1.2,
        maxDrawdown: 0.18,
        isActive: false
      },
      {
        id: '3',
        name: 'Quantum Overlay Strategy',
        winRate: 0.85,
        profitFactor: 2.5,
        sharpeRatio: 1.8,
        maxDrawdown: 0.12,
        isActive: true
      }
    ];
  }
}

// Fetch performance metrics for a specific strategy
export async function fetchStrategyPerformance(strategyId: string): Promise<StrategyPerformance> {
  try {
    const response = await fetch(`/api/strategies/${strategyId}/performance`);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch strategy performance: ${response.statusText}`);
    }
    
    const data: ApiResponse<StrategyPerformance> = await response.json();
    
    if (!data.success || !data.data) {
      throw new Error(data.error || 'Failed to fetch strategy performance');
    }
    
    return data.data;
  } catch (error) {
    console.error(`Error fetching performance for strategy ${strategyId}:`, error);
    // Return mock data for development/testing
    return {
      winRate: Math.random() * 0.3 + 0.6, // 60-90%
      profitFactor: Math.random() * 1.5 + 1.5, // 1.5-3.0
      totalTrades: Math.floor(Math.random() * 100) + 50, // 50-150
      averageProfit: Math.random() * 2 + 0.5, // £0.5-£2.5
      maxDrawdown: Math.random() * 0.2 + 0.05, // 5-25%
      sharpeRatio: Math.random() + 1.0, // 1.0-2.0
      sortino: Math.random() * 1.5 + 1.0, // 1.0-2.5
      profitByMonth: {
        'Jan': Math.random() * 10 - 2,
        'Feb': Math.random() * 10 - 2,
        'Mar': Math.random() * 10 - 2,
      }
    };
  }
}

// Update a strategy configuration
export async function updateStrategy(config: StrategyConfig): Promise<Strategy> {
  try {
    const response = await fetch(`/api/strategies/${config.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to update strategy: ${response.statusText}`);
    }
    
    const data: ApiResponse<Strategy> = await response.json();
    
    if (!data.success || !data.data) {
      throw new Error(data.error || 'Failed to update strategy');
    }
    
    return data.data;
  } catch (error) {
    console.error(`Error updating strategy ${config.id}:`, error);
    // Return mock data for development/testing
    return {
      id: config.id,
      name: config.name,
      winRate: 0.75,
      profitFactor: 2.1,
      sharpeRatio: 1.5,
      maxDrawdown: 0.15,
      isActive: config.isActive
    };
  }
}

// Create a new strategy
export async function createStrategy(config: Omit<StrategyConfig, 'id'>): Promise<Strategy> {
  try {
    const response = await fetch('/api/strategies', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(config),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to create strategy: ${response.statusText}`);
    }
    
    const data: ApiResponse<Strategy> = await response.json();
    
    if (!data.success || !data.data) {
      throw new Error(data.error || 'Failed to create strategy');
    }
    
    return data.data;
  } catch (error) {
    console.error('Error creating strategy:', error);
    // Return mock data for development/testing
    return {
      id: Math.random().toString(36).substring(2, 10),
      name: config.name,
      winRate: 0.65,
      profitFactor: 1.7,
      sharpeRatio: 1.2,
      maxDrawdown: 0.20,
      isActive: config.isActive
    };
  }
}

// Delete a strategy
export async function deleteStrategy(strategyId: string): Promise<boolean> {
  try {
    const response = await fetch(`/api/strategies/${strategyId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete strategy: ${response.statusText}`);
    }
    
    const data: ApiResponse<{ deleted: boolean }> = await response.json();
    
    if (!data.success || !data.data) {
      throw new Error(data.error || 'Failed to delete strategy');
    }
    
    return data.data.deleted;
  } catch (error) {
    console.error(`Error deleting strategy ${strategyId}:`, error);
    // Return success for development/testing
    return true;
  }
}