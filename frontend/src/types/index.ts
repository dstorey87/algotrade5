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

export interface Trade {
  id: string;
  pair: string;
  type: 'buy' | 'sell';
  amount: number;
  price: number;
  timestamp: string;
  status: 'open' | 'closed' | 'cancelled';
  profit?: number;
  strategy: string;
  confidence: number;
}

export interface WSMessage {
  type: 'trade' | 'strategy' | 'error' | 'system';
  data: Trade | any;
  timestamp: string;
}

export interface Strategy {
  id: string;
  name: string;
  code: string;
  parameters: Record<string, any>;
  isActive: boolean;
  performance: {
    totalTrades: number;
    winRate: number;
    profitFactor: number;
    drawdown: number;
  };
  lastUpdated: string;
  createdAt: string;
}

export interface StrategyConfig {
  id: string; // Making id required to match StrategyUpdate
  name: string;
  code: string;
  parameters: Record<string, any>;
  isActive: boolean;
  maxOpenTrades: number;
  stakeAmount: number;
  minRoi: Record<string, number>;
  stopLoss: number;
  trailingStop: boolean;
  trailingStopPositive: number;
}
