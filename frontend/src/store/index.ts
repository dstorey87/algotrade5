import { configureStore } from '@reduxjs/toolkit'
import systemReducer from './slices/systemSlice'
import tradingReducer from './slices/tradingSlice'

export const store = configureStore({
  reducer: {
    system: systemReducer,
    trading: tradingReducer
  }
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch