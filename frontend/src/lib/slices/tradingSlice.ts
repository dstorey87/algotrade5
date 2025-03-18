import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

export interface SystemStatus {
  freqtrade: boolean
  database: boolean
  models: boolean
  quantum: boolean
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
  open_date?: string
  close_date?: string
  is_open?: boolean
}

export interface PerformanceStats {
  winRate: number
  drawdown: number
  tradesToday: number
  winStreak: number
  modelPerformance: number
}

interface Balance {
  total: number
  free: number
  used: number
  currency: string
}

interface TradingState {
  tradingEnabled: boolean
  systemStatus: SystemStatus
  balance: Balance
  totalProfit: number
  winRate: number
  activeTrades: number
  activeTradesList: Trade[]
  tradeHistory: Trade[]
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
  lastUpdated: number | null
  realTimeEnabled: boolean
}

const initialState: TradingState = {
  tradingEnabled: false,
  systemStatus: {
    freqtrade: false,
    database: false,
    models: false,
    quantum: false,
  },
  balance: {
    total: 10,
    free: 10,
    used: 0,
    currency: 'GBP'
  },
  totalProfit: 0,
  winRate: 0,
  activeTrades: 0,
  activeTradesList: [],
  tradeHistory: [],
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
  lastUpdated: null,
  realTimeEnabled: false
}

export const fetchTradeData = createAsyncThunk(
  'trading/fetchTradeData',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/status')
      const data = await response.json()
      return data
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const startTrading = createAsyncThunk(
  'trading/startTrading',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/start', { method: 'POST' })
      const data = await response.json()
      return data
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

export const stopTrading = createAsyncThunk(
  'trading/stopTrading',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/stop', { method: 'POST' })
      const data = await response.json()
      return data
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

// New thunk for fetching current trades
export const fetchCurrentTrades = createAsyncThunk(
  'trading/fetchCurrentTrades',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/status/active_trades')
      const data = await response.json()
      return data
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

// New thunk for fetching trade history
export const fetchTradeHistory = createAsyncThunk(
  'trading/fetchTradeHistory',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/v1/status/completed_trades')
      const data = await response.json()
      return data
    } catch (error: any) {
      return rejectWithValue(error.message)
    }
  }
)

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    updateCurrentPrices: (state, action) => {
      state.activeTradesList = state.activeTradesList.map(trade => ({
        ...trade,
        currentPrice: action.payload[trade.pair] || trade.currentPrice,
        unrealizedProfit: ((action.payload[trade.pair] || trade.currentPrice || 0) - trade.entryPrice) * trade.amount,
        unrealizedProfitPercentage: ((action.payload[trade.pair] || trade.currentPrice || 0) - trade.entryPrice) / trade.entryPrice * 100
      }))
      state.lastUpdated = Date.now();
    },
    
    // New actions for WebSocket updates
    setRealTimeEnabled: (state, action) => {
      state.realTimeEnabled = action.payload;
    },
    
    updateActiveTrades: (state, action) => {
      state.activeTradesList = action.payload;
      state.activeTrades = action.payload.length;
      state.lastUpdated = Date.now();
    },
    
    updateTradeHistory: (state, action) => {
      state.tradeHistory = action.payload;
      
      // Calculate win rate based on closed trades
      if (action.payload.length > 0) {
        const winningTrades = action.payload.filter(trade => trade.profit && trade.profit > 0).length;
        state.winRate = winningTrades / action.payload.length;
      }
      
      state.lastUpdated = Date.now();
    },
    
    updateBalance: (state, action) => {
      state.balance = action.payload;
      state.lastUpdated = Date.now();
    },
    
    updatePerformanceStats: (state, action) => {
      const { winRate, drawdown, tradesToday, winStreak, modelPerformance, totalProfit } = action.payload;
      
      if (winRate !== undefined) state.winRate = winRate;
      if (drawdown !== undefined) state.drawdown = drawdown;
      if (tradesToday !== undefined) state.tradesToday = tradesToday;
      if (winStreak !== undefined) state.winStreak = winStreak;
      if (modelPerformance !== undefined) state.modelPerformance = modelPerformance;
      if (totalProfit !== undefined) state.totalProfit = totalProfit;
      
      state.lastUpdated = Date.now();
    },
    
    setError: (state, action) => {
      state.error = action.payload;
    },
    
    clearError: (state) => {
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTradeData.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchTradeData.fulfilled, (state, action) => {
        state.isLoading = false;
        // Merge the data with existing state
        if (action.payload) {
          if (action.payload.systemStatus) state.systemStatus = action.payload.systemStatus;
          if (action.payload.balance) state.balance = action.payload.balance;
          if (action.payload.totalProfit !== undefined) state.totalProfit = action.payload.totalProfit;
          if (action.payload.winRate !== undefined) state.winRate = action.payload.winRate;
          if (action.payload.tradingEnabled !== undefined) state.tradingEnabled = action.payload.tradingEnabled;
          if (action.payload.activeStrategy) state.activeStrategy = action.payload.activeStrategy;
          
          state.lastUpdated = Date.now();
        }
      })
      .addCase(fetchTradeData.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      })
      .addCase(startTrading.fulfilled, (state) => {
        state.tradingEnabled = true;
      })
      .addCase(stopTrading.fulfilled, (state) => {
        state.tradingEnabled = false;
      })
      .addCase(fetchCurrentTrades.fulfilled, (state, action) => {
        state.activeTradesList = action.payload;
        state.activeTrades = action.payload.length;
        state.lastUpdated = Date.now();
      })
      .addCase(fetchTradeHistory.fulfilled, (state, action) => {
        state.tradeHistory = action.payload;
        
        // Calculate win rate based on closed trades
        if (action.payload.length > 0) {
          const winningTrades = action.payload.filter(trade => trade.profit && trade.profit > 0).length;
          state.winRate = winningTrades / action.payload.length;
        }
        
        state.lastUpdated = Date.now();
      })
  },
})

export const { 
  updateCurrentPrices, 
  setRealTimeEnabled, 
  updateActiveTrades, 
  updateTradeHistory, 
  updateBalance, 
  updatePerformanceStats, 
  setError, 
  clearError 
} = tradingSlice.actions

export default tradingSlice.reducer
