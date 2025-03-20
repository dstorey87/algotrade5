export interface AIMetrics {
  modelName: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  confidence: number;
  timestamp: string;
}

export interface QuantumState {
  confidence: number;
  currentPattern: string;
  activeStates: number;
  lastUpdated: string;
}

export interface TradingState {
  tradingEnabled: boolean;
  systemStatus: {
    freqtrade: boolean;
    database: boolean;
    models: boolean;
    quantum: boolean;
  };
  balance: {
    total: number;
    free: number;
    used: number;
  };
  totalProfit: number;
  winRate: number;
  activeTrades: number;
  trades: Array<any>; // TODO: Define proper Trade interface
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
  aiMetrics: AIMetrics;
  quantum: QuantumState;
}

export interface RootState {
  trading: TradingState;
}