import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

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
  tradeHistory: []
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

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    resetError: (state) => {
      state.error = null
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
  }
})

export const { resetError } = tradingSlice.actions
export default tradingSlice.reducer