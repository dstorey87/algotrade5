import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { tradingApi } from '../../services/api'

export interface Trade {
  id: number
  timestamp: string
  pair: string
  type: 'buy' | 'sell'
  entryPrice: number
  exitPrice: number
  amount: number
  profit: number
  profitPercentage: number
  strategy: string
  confidence: number
  patternValidated: boolean
  quantumValidated: boolean
  tags: string[]
}

interface SystemStatus {
  freqtrade: boolean
  database: boolean
  models: boolean
  quantum: boolean
}

export interface TradingState {
  tradingEnabled: boolean
  systemStatus: SystemStatus
  balance: {
    total: number
    free: number
    used: number
    stake: number
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
    total: Number(import.meta.env.VITE_INITIAL_CAPITAL),
    free: Number(import.meta.env.VITE_INITIAL_CAPITAL),
    used: 0,
    stake: Number(import.meta.env.VITE_INITIAL_CAPITAL),
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
      const [statusResponse, balanceResponse, tradesResponse] = await Promise.all([
        tradingApi.getSystemStatus(),
        tradingApi.getBalance(),
        tradingApi.getTrades()
      ])

      const status = statusResponse.data
      const balance = balanceResponse.data
      const trades = tradesResponse.data

      // Calculate derived metrics
      const winningTrades = trades.filter(t => t.profit > 0)
      const winRate = trades.length > 0 ? winningTrades.length / trades.length : 0
      const totalProfit = trades.reduce((sum, t) => sum + t.profit, 0)
      const activeTrades = trades.filter(t => !t.exitPrice).length
      
      // Calculate win streak
      let winStreak = 0
      for (let i = trades.length - 1; i >= 0; i--) {
        if (trades[i].profit > 0) winStreak++
        else break
      }

      // Get today's trades
      const today = new Date().toISOString().split('T')[0]
      const tradesToday = trades.filter(t => 
        t.timestamp.startsWith(today)
      ).length

      return {
        tradingEnabled: status.running,
        systemStatus: {
          freqtrade: true,
          database: true,
          models: status.model_loaded,
          quantum: status.quantum_ready,
        },
        balance,
        totalProfit,
        winRate,
        activeTrades,
        trades,
        activeStrategy: status.strategy,
        drawdown: status.max_drawdown,
        confidence: status.confidence,
        patternValidation: status.pattern_validated,
        quantumValidation: status.quantum_validated,
        tradesToday,
        winStreak,
        modelPerformance: status.model_performance,
      }
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to fetch trade data')
    }
  }
)

export const startTrading = createAsyncThunk(
  'trading/startTrading',
  async (_, { rejectWithValue }) => {
    try {
      const response = await tradingApi.startTrading()
      return response.data
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to start trading')
    }
  }
)

export const stopTrading = createAsyncThunk(
  'trading/stopTrading',
  async (_, { rejectWithValue }) => {
    try {
      const response = await tradingApi.stopTrading()
      return response.data
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to stop trading')
    }
  }
)

export const emergencyStop = createAsyncThunk(
  'trading/emergencyStop',
  async (_, { rejectWithValue }) => {
    try {
      const response = await tradingApi.emergencyStop()
      return response.data
    } catch (error: any) {
      return rejectWithValue(error.message || 'Failed to execute emergency stop')
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
      
      .addCase(startTrading.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(startTrading.fulfilled, (state, action) => {
        state.isLoading = false
        state.tradingEnabled = action.payload.status === 'running'
      })
      .addCase(startTrading.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      
      .addCase(stopTrading.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(stopTrading.fulfilled, (state, action) => {
        state.isLoading = false
        state.tradingEnabled = action.payload.status === 'running'
      })
      .addCase(stopTrading.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      
      .addCase(emergencyStop.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(emergencyStop.fulfilled, (state, action) => {
        state.isLoading = false
        state.tradingEnabled = false
      })
      .addCase(emergencyStop.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
  },
})

export const { resetError } = tradingSlice.actions

export default tradingSlice.reducer