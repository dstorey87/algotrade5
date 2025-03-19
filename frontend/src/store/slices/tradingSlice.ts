import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { TradingState, AIMetrics } from '../../types/trading';

interface TradingState {
  isLoading: boolean
  error: string | null
  tradingEnabled: boolean
  balance: {
    total: number
    free: number
    used: number
  }
  currentTrade: {
    pair: string
    side: 'buy' | 'sell'
    amount: number
    entryPrice: number
    currentPrice: number
    profitLoss: number
  } | null
  openPositions: Array<{
    pair: string
    side: 'buy' | 'sell'
    amount: number
    entryPrice: number
    currentPrice: number
    profitLoss: number
  }>
  tradeHistory: Array<{
    pair: string
    side: 'buy' | 'sell'
    amount: number
    entryPrice: number
    exitPrice: number
    profitLoss: number
    timestamp: string
  }>
  isConnected: boolean
  currentStrategy: string | null
  aiMetrics: AIMetrics
}

const initialState: TradingState = {
  isLoading: false,
  error: null,
  tradingEnabled: false,
  balance: {
    total: 0,
    free: 0,
    used: 0
  },
  currentTrade: null,
  openPositions: [],
  tradeHistory: [],
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
  }
}

export const fetchTradeData = createAsyncThunk(
  'trading/fetchData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/trading/status')
      if (!response.ok) throw new Error('Failed to fetch trading data')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch trading data')
    }
  }
)

export const startTrading = createAsyncThunk(
  'trading/start',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/trading/start', { method: 'POST' })
      if (!response.ok) throw new Error('Failed to start trading')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to start trading')
    }
  }
)

export const stopTrading = createAsyncThunk(
  'trading/stop',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/trading/stop', { method: 'POST' })
      if (!response.ok) throw new Error('Failed to stop trading')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to stop trading')
    }
  }
)

export const fetchDashboardData = createAsyncThunk(
  'trading/fetchDashboardData',
  async () => {
    try {
      // TODO: Replace with actual API call
      const response = await Promise.resolve({
        balance: {
          total: 1000,
          free: 800,
          used: 200
        },
        openPositions: [],
        tradeHistory: []
      });
      return response;
    } catch (error) {
      throw error;
    }
  }
);

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    resetError: (state) => {
      state.error = null
    },
    setConnection: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    },
    updateAIMetrics: (state, action: PayloadAction<Partial<AIMetrics>>) => {
      state.aiMetrics = { ...state.aiMetrics, ...action.payload };
    },
    setCurrentStrategy: (state, action: PayloadAction<string>) => {
      state.currentStrategy = action.payload;
    },
    updateBalance: (state, action: PayloadAction<number>) => {
      state.balance = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTradeData.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchTradeData.fulfilled, (state, action) => {
        state.isLoading = false
        Object.assign(state, action.payload)
      })
      .addCase(fetchTradeData.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(startTrading.fulfilled, (state) => {
        state.tradingEnabled = true
      })
      .addCase(stopTrading.fulfilled, (state) => {
        state.tradingEnabled = false
      })
      .addCase(fetchDashboardData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.isLoading = false;
        state.balance = action.payload.balance;
        state.openPositions = action.payload.openPositions;
        state.tradeHistory = action.payload.tradeHistory;
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch dashboard data';
      });
  }
})

export const { resetError, setConnection, updateAIMetrics, setCurrentStrategy, updateBalance } = tradingSlice.actions
export default tradingSlice.reducer
