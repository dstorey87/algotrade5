import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { TradingState, AIMetrics, QuantumState } from './types';

const initialState: TradingState = {
  tradingEnabled: false,
  systemStatus: {
    freqtrade: false,
    database: false,
    models: false,
    quantum: false
  },
  balance: {
    total: 0,
    free: 0,
    used: 0
  },
  totalProfit: 0,
  winRate: 0,
  activeTrades: 0,
  trades: [],
  activeStrategy: null,
  drawdown: 0,
  confidence: 0,
  patternValidation: false,
  quantumValidation: false,
  tradesToday: 0,
  winStreak: 0,
  modelPerformance: 0,
  isLoading: false,
  error: null,
  aiMetrics: {
    modelName: 'QuantumHybrid-v1',
    accuracy: 0.85,
    precision: 0.82,
    recall: 0.87,
    f1Score: 0.84,
    confidence: 0.89,
    timestamp: new Date().toISOString()
  },
  quantum: {
    confidence: 0.91,
    currentPattern: 'Quantum Entanglement',
    activeStates: 24,
    lastUpdated: new Date().toISOString()
  }
};

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    updateAIMetrics: (state, action: PayloadAction<AIMetrics>) => {
      state.aiMetrics = action.payload;
    },
    updateQuantumState: (state, action: PayloadAction<QuantumState>) => {
      state.quantum = action.payload;
    },
    updateTradingState: (state, action: PayloadAction<Partial<TradingState>>) => {
      return { ...state, ...action.payload };
    },
    startTrading: (state) => {
      state.tradingEnabled = true;
      state.error = null;
    },
    stopTrading: (state) => {
      state.tradingEnabled = false;
      state.error = null;
    },
    emergencyStop: (state) => {
      state.tradingEnabled = false;
      state.activeTrades = 0;
      state.trades = state.trades.map(trade => 
        trade.status === 'open' ? { ...trade, status: 'cancelled' } : trade
      );
      state.error = 'Emergency stop initiated - all trades cancelled';
    }
  }
});

export const { 
  updateAIMetrics, 
  updateQuantumState, 
  updateTradingState,
  startTrading,
  stopTrading,
  emergencyStop
} = tradingSlice.actions;

export default tradingSlice.reducer;