import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { AIMetrics, Trade } from '@/types'

export interface SystemStatus {
  freqtrade: boolean
  database: boolean
  models: boolean
  quantum: boolean
}

export interface PerformanceStats {
  wins: number
  losses: number
  totalProfit: number
  totalLoss: number
  trades: number
}

export interface Balance {
  total: number
  free: number
  used: number
}

export interface TradingState {
  isLoading: boolean
  error: string | null
  tradingEnabled: boolean
  systemStatus: SystemStatus
  balance: Balance
  currentTrade: Trade | null
  trades: Trade[]
  openPositions: Trade[]
  tradeHistory: Trade[]
  performanceStats: PerformanceStats
  realTimeEnabled: boolean
  isConnected: boolean
  currentStrategy: string | null
  aiMetrics: AIMetrics
}

const initialState: TradingState = {
  isLoading: false,
  error: null,
  tradingEnabled: false,
  systemStatus: {
    freqtrade: false,
    database: false,
    models: false,
    quantum: false,
  },
  balance: {
    total: 0,
    free: 0,
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

export const fetchCurrentTrades = createAsyncThunk(
  'trading/fetchCurrentTrades',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/status/active_trades')
      if (!response.ok) throw new Error('Failed to fetch current trades')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch current trades')
    }
  }
)

export const fetchTradeHistory = createAsyncThunk(
  'trading/fetchTradeHistory',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/status/completed_trades')
      if (!response.ok) throw new Error('Failed to fetch trade history')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch trade history')
    }
  }
)

export const fetchDashboardData = createAsyncThunk(
  'trading/fetchDashboardData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/dashboard')
      if (!response.ok) throw new Error('Failed to fetch dashboard data')
      return await response.json()
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch dashboard data')
    }
  }
)

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    resetError: (state) => {
      state.error = null
    },
    setConnection: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload
    },
    updateAIMetrics: (state, action: PayloadAction<Partial<AIMetrics>>) => {
      state.aiMetrics = { ...state.aiMetrics, ...action.payload }
    },
    setCurrentStrategy: (state, action: PayloadAction<string>) => {
      state.currentStrategy = action.payload
    },
    updateBalance: (state, action: PayloadAction<Balance>) => {
      state.balance = action.payload
    },
    updateSystemStatus: (state, action: PayloadAction<Partial<SystemStatus>>) => {
      state.systemStatus = { ...state.systemStatus, ...action.payload }
    },
    updateTrades: (state, action: PayloadAction<Trade[]>) => {
      state.trades = action.payload
    },
    updatePerformanceStats: (state, action: PayloadAction<PerformanceStats>) => {
      state.performanceStats = action.payload
    },
    setRealTimeEnabled: (state, action: PayloadAction<boolean>) => {
      state.realTimeEnabled = action.payload
    },
    emergencyStop: (state) => {
      state.tradingEnabled = false
      state.trades = state.trades.map(trade => 
        trade.status === 'open' ? { ...trade, status: 'cancelled' } : trade
      )
      state.error = 'Emergency stop initiated - all trades cancelled'
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
        if (action.payload) {
          if (action.payload.systemStatus) state.systemStatus = action.payload.systemStatus
          if (action.payload.balance) state.balance = action.payload.balance
          if (action.payload.performanceStats) state.performanceStats = action.payload.performanceStats
          if (action.payload.tradingEnabled !== undefined) state.tradingEnabled = action.payload.tradingEnabled
        }
      })
      .addCase(fetchTradeData.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(startTrading.fulfilled, (state) => {
        state.tradingEnabled = true
        state.error = null
      })
      .addCase(stopTrading.fulfilled, (state) => {
        state.tradingEnabled = false
        state.error = null
      })
      .addCase(fetchCurrentTrades.fulfilled, (state, action) => {
        state.trades = action.payload
      })
      .addCase(fetchTradeHistory.fulfilled, (state, action) => {
        state.tradeHistory = action.payload
      })
      .addCase(fetchDashboardData.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchDashboardData.fulfilled, (state, action) => {
        state.isLoading = false
        state.balance = action.payload.balance
        state.openPositions = action.payload.openPositions
        state.tradeHistory = action.payload.tradeHistory
      })
      .addCase(fetchDashboardData.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.error.message || 'Failed to fetch dashboard data'
      })
  }
})

export const {
  resetError,
  setConnection,
  updateAIMetrics,
  setCurrentStrategy,
  updateBalance,
  updateSystemStatus,
  updateTrades,
  updatePerformanceStats,
  setRealTimeEnabled,
  emergencyStop
} = tradingSlice.actions

export default tradingSlice.reducer
