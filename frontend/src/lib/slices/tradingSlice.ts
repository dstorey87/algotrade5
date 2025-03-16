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
}

interface TradingState {
  tradingEnabled: boolean
  systemStatus: SystemStatus
  balance: {
    total: number
    free: number
    used: number
  }
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

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    updateCurrentPrices: (state, action) => {
      state.trades = state.trades.map(trade => !trade.exitPrice ? {
        ...trade,
        currentPrice: action.payload[trade.pair],
        unrealizedProfit: (action.payload[trade.pair] - trade.entryPrice) * trade.amount,
        unrealizedProfitPercentage: ((action.payload[trade.pair] - trade.entryPrice) / trade.entryPrice) * 100
      } : trade)
    },
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
  },
})

export const { updateCurrentPrices } = tradingSlice.actions
export default tradingSlice.reducer
