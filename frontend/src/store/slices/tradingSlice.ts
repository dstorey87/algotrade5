import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Trade {
  id: string
  pair: string
  type: 'buy' | 'sell'
  amount: number
  price: number
}

interface TradingState {
  balance: number
  activeStrategy: string | null
  winRate: number
  drawdown: number
  trades: Trade[]
  isTrading: boolean
  lastError: string | null
}

const initialState: TradingState = {
  balance: 10,
  activeStrategy: null,
  winRate: 0,
  drawdown: 0,
  trades: [],
  isTrading: false,
  lastError: null
}

const tradingSlice = createSlice({
  name: 'trading',
  initialState,
  reducers: {
    updateBalance(state, action: PayloadAction<number>) {
      state.balance = action.payload
    },
    setActiveStrategy(state, action: PayloadAction<string | null>) {
      state.activeStrategy = action.payload
    },
    updateMetrics(state, action: PayloadAction<{ winRate: number; drawdown: number }>) {
      state.winRate = action.payload.winRate
      state.drawdown = action.payload.drawdown
    },
    addTrade(state, action: PayloadAction<Trade>) {
      state.trades.push(action.payload)
    },
    setTrading(state, action: PayloadAction<boolean>) {
      state.isTrading = action.payload
    },
    setError(state, action: PayloadAction<string | null>) {
      state.lastError = action.payload
    }
  }
})

export const { 
  updateBalance,
  setActiveStrategy,
  updateMetrics,
  addTrade,
  setTrading,
  setError
} = tradingSlice.actions

export default tradingSlice.reducer