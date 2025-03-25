import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface Trade {
  id: string;
  pair: string;
  type: 'buy' | 'sell';
  profit: number;
  timestamp: string;
}

interface PerformanceMetrics {
  messageProcessingRate: number;
  batchSize: number;
  compressionRatio: number;
  latency: number;
}

interface TradingState {
  trades: Trade[];
  performanceMetrics: PerformanceMetrics;
}

const initialState: TradingState = {
  trades: [],
  performanceMetrics: {
    messageProcessingRate: 0,
    batchSize: 0,
    compressionRatio: 0,
    latency: 0
  }
};

export const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    updateTrades: (state, action: PayloadAction<Trade[]>) => {
      state.trades = action.payload;
    },
    updatePerformanceMetrics: (state, action: PayloadAction<PerformanceMetrics>) => {
      state.performanceMetrics = action.payload;
    }
  }
});

export const { updateTrades, updatePerformanceMetrics } = tradingSlice.actions;
export default tradingSlice.reducer;
