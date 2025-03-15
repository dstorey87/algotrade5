import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import TradingControls from './index'
import tradingReducer from '../../store/slices/tradingSlice'

const createTestStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      trading: tradingReducer
    },
    preloadedState: {
      trading: {
        balance: 100.50,
        totalProfit: 25.75,
        winRate: 0.85,
        activeTrades: 3,
        ...initialState
      }
    }
  })
}

describe('TradingControls', () => {
  it('renders account status correctly', () => {
    render(
      <Provider store={createTestStore()}>
        <TradingControls />
      </Provider>
    )
    
    expect(screen.getByText('Trading Controls')).toBeInTheDocument()
    expect(screen.getByText('Balance: £100.50')).toBeInTheDocument()
    expect(screen.getByText('Total Profit: £25.75')).toBeInTheDocument()
    expect(screen.getByText('Win Rate: 85.00%')).toBeInTheDocument()
    expect(screen.getByText('Active Trades: 3')).toBeInTheDocument()
  })

  it('displays trading control buttons', () => {
    render(
      <Provider store={createTestStore()}>
        <TradingControls />
      </Provider>
    )
    
    expect(screen.getByText('Start Trading')).toBeInTheDocument()
    expect(screen.getByText('Stop Trading')).toBeInTheDocument()
  })

  it('handles button clicks', () => {
    const consoleSpy = vitest.spyOn(console, 'log')
    
    render(
      <Provider store={createTestStore()}>
        <TradingControls />
      </Provider>
    )
    
    fireEvent.click(screen.getByText('Start Trading'))
    expect(consoleSpy).toHaveBeenCalledWith('Starting trading...')
    
    fireEvent.click(screen.getByText('Stop Trading'))
    expect(consoleSpy).toHaveBeenCalledWith('Stopping trading...')
  })
})