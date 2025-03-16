export interface RootState {
  trading: TradingState
}

export interface TradingState {
  tradingEnabled: boolean
  systemStatus: SystemStatus
  balance: Balance
  totalProfit: number
  winRate: number
  activeTrades: number
  trades: Trade[]
  activeStrategy: string | null
  drawdown: number
  confidence: number
  patternValidation: boolean
  quantumValidation: boolean
  tradesToday: number
  winStreak: number
  modelPerformance: number
  isLoading: boolean
  error: string | null
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
  id: string
  pair: string
  type: 'buy' | 'sell'
  amount: number
  entryPrice: number
  currentPrice?: number
  exitPrice?: number
  unrealizedProfit?: number
  unrealizedProfitPercentage?: number
  profit?: number
  profitPercentage?: number
  strategy: string
  confidence: number
  patternValidated: boolean
  quantumValidated: boolean
  timestamp: string
}
