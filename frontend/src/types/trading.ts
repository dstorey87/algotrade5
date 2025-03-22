export interface Balance {
  total: number;
  free: number;
  used: number;
}

export interface AIMetrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  latency: number;
  ensembleAccuracy: number;
  activeModels: number;
  trainingInProgress: boolean;
}

export interface TradingMetrics {
  aiConfidence: number;
  predictionAccuracy: number;
  quantum?: {
    loopStatus: string;
  };
  // Adding other potential fields based on component usage
  winRate?: number;
  profitLoss?: number;
  activeStrategies?: number;
  tradingVolume?: number;
}

export interface TradingState {
  isConnected: boolean;
  currentStrategy: string | null;
  balance: Balance;
  aiMetrics: AIMetrics;
  // ... other trading state properties
}