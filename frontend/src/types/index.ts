export interface RootState {
  trading: TradingState
}

export interface TradingState {
  tradingEnabled: boolean;
  systemStatus: SystemStatus;
  balance: Balance;
  totalProfit: number;
  winRate: number;
  activeTrades: number;
  trades: Trade[];
  activeStrategy: string | null;
  drawdown: number;
  confidence: number;
  patternValidation: boolean;
  quantumValidation: boolean;
  tradesToday: number;
  winStreak: number;
  modelPerformance: number;
  isLoading: boolean;
  error: string | null;
  performanceStats: {
    wins: number;
    losses: number;
    totalProfit: number;
    totalLoss: number;
    trades: number;
  };
  realTimeEnabled: boolean;
}

export interface SystemStatus {
  freqtrade: boolean
  database: boolean
  models: boolean
  quantum: boolean
}

export interface Balance {
  total: number
  free: number
  used: number
}

// Trade types
export interface Trade {
  id: string;
  pair: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number;
  timestamp?: number;
  profit?: number;
  profitPercentage?: number;
  strategyId?: string;
  status: 'open' | 'closed' | 'cancelled';
  strategy: string;
  confidence: number;
}

export interface WSMessage {
  type: 'trade' | 'strategy' | 'error' | 'system';
  data: Trade | any;
  timestamp: string;
}

// Basic strategy types
export interface Strategy {
  id: string;
  name: string;
  winRate: number;
  profitFactor: number;
  sharpeRatio: number;
  maxDrawdown: number;
  isActive?: boolean;
  performance?: StrategyPerformance;
  parameters?: Record<string, any>;
}

// Strategy configuration types
export interface StrategyConfig {
  id: string;
  name: string;
  code?: string;
  parameters: Record<string, any>;
  isActive: boolean;
  maxOpenTrades: number;
  stakeAmount: number;
  minRoi: Record<string, number>;
  stopLoss: number;
  trailingStop: boolean;
  trailingStopPositive?: number;
}

// Performance metrics for strategies
export interface StrategyPerformance {
  winRate: number;
  profitFactor: number;
  totalTrades: number;
  averageProfit: number;
  maxDrawdown: number;
  sharpeRatio?: number;
  sortino?: number;
  profitByMonth?: Record<string, number>;
}

// Market data types
export interface MarketData {
  pair: string;
  price: number;
  volume: number;
  high24h: number;
  low24h: number;
  change24h: number;
  timestamp: number;
}

// System metrics
export interface SystemMetrics {
  cpuUsage: number;
  memoryUsage: number;
  diskSpace: number;
  networkLatency: number;
  apiCallsPerMinute: number;
  lastUpdated: number;
}

// User types
export interface User {
  id: string;
  username: string;
  email: string;
  preferences: UserPreferences;
}

// User preferences
export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  notifications: boolean;
  riskLevel: 'low' | 'medium' | 'high';
  currency: string;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export type ModelType = 'ml' | 'llm' | 'quantum';

export interface ModelStatus {
  isLoaded: boolean;
  isLoading: boolean;
  loadedAt?: number;
  lastUsed?: number;
}

export interface AIMetrics {
  accuracy: number
  precision: number
  recall: number
  f1Score: number
  latency: number
  ensembleAccuracy: number
  activeModels: number
  trainingInProgress: boolean
}
