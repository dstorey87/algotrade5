import { configureStore } from '@reduxjs/toolkit';
import tradingReducer from '@/store/slices/tradingSlice';
import systemReducer from '@/store/slices/systemSlice';
import type { TradingState } from '@/store/slices/tradingSlice';
import type { SystemState } from '@/store/slices/systemSlice';

interface TestStoreState {
  trading?: Partial<TradingState>;
  system?: Partial<SystemState>;
}

export const createTestStore = (initialState: TestStoreState = {}) => {
  return configureStore({
    reducer: {
      trading: tradingReducer,
      system: systemReducer
    },
    preloadedState: {
      trading: {
        isLoading: false,
        error: null,
        tradingEnabled: false,
        systemStatus: {
          freqtrade: false,
          database: false,
          models: false,
          quantum: false
        },
        balance: {
          total: 10.00,
          free: 10.00,
          used: 0
        },
        currentTrade: null,
        trades: [],
        openPositions: [],
        tradeHistory: [],
        performanceStats: {
          wins: 0,
          losses: 0,
          totalProfit: 0,
          totalLoss: 0,
          trades: 0
        },
        realTimeEnabled: false,
        isConnected: false,
        currentStrategy: null,
        aiMetrics: {
          accuracy: 0,
          precision: 0,
          recall: 0,
          f1Score: 0,
          latency: 0,
          ensembleAccuracy: 0,
          activeModels: 0,
          trainingInProgress: false
        },
        ...initialState.trading
      },
      system: {
        isLoading: false,
        error: null,
        status: 'stopped' as const,
        version: '1.0.0',
        uptime: '0:00:00',
        dryRun: true,
        tradingMode: 'spot',
        gpuUtilization: 0,
        memoryUsage: 0,
        systemHealth: {
          freqtrade: true,
          database: true,
          models: true,
          quantum: true,
        },
        logs: [],
        ...initialState.system
      }
    }
  });
};