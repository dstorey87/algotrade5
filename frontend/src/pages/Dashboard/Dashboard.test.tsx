import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import systemReducer from '../../store/slices/systemSlice'
import Dashboard from './index'

const createTestStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      system: systemReducer
    },
    preloadedState: {
      system: {
        gpuUtilization: 45.5,
        memoryUsage: 60.2,
        modelAccuracy: 0.87,
        modelConfidence: 0.92,
        quantumCircuitStatus: 'Ready',
        systemHealth: {
          freqtrade: true,
          database: true,
          models: true,
          quantum: true
        },
        ...initialState
      }
    }
  })
}

describe('Dashboard', () => {
  it('renders system overview section', () => {
    render(
      <Provider store={createTestStore()}>
        <Dashboard />
      </Provider>
    )

    expect(screen.getByText('System Overview')).toBeInTheDocument()
  })

  it('displays resource usage metrics', () => {
    render(
      <Provider store={createTestStore()}>
        <Dashboard />
      </Provider>
    )

    expect(screen.getByText(/GPU: 45.50%/)).toBeInTheDocument()
    expect(screen.getByText(/Memory: 60.20%/)).toBeInTheDocument()
  })

  it('shows model performance statistics', () => {
    render(
      <Provider store={createTestStore()}>
        <Dashboard />
      </Provider>
    )

    expect(screen.getByText(/Accuracy: 87.00%/)).toBeInTheDocument()
    expect(screen.getByText(/Confidence: 92.00%/)).toBeInTheDocument()
  })

  it('displays quantum circuit status', () => {
    render(
      <Provider store={createTestStore()}>
        <Dashboard />
      </Provider>
    )

    expect(screen.getByText('Quantum Circuit')).toBeInTheDocument()
    expect(screen.getByText(/Status: Ready/)).toBeInTheDocument()
  })

  it('shows system health indicators', () => {
    render(
      <Provider store={createTestStore()}>
        <Dashboard />
      </Provider>
    )

    expect(screen.getByText('FreqTrade: Online')).toBeInTheDocument()
    expect(screen.getByText('Database: Connected')).toBeInTheDocument()
    expect(screen.getByText('Models: Loaded')).toBeInTheDocument()
    expect(screen.getByText('Quantum: Ready')).toBeInTheDocument()
  })

  it('handles offline system components', () => {
    render(
      <Provider store={createTestStore({
        systemHealth: {
          freqtrade: false,
          database: false,
          models: false,
          quantum: false
        }
      })}>
        <Dashboard />
      </Provider>
    )

    expect(screen.getByText('FreqTrade: Offline')).toBeInTheDocument()
    expect(screen.getByText('Database: Disconnected')).toBeInTheDocument()
    expect(screen.getByText('Models: Not Loaded')).toBeInTheDocument()
    expect(screen.getByText('Quantum: Not Ready')).toBeInTheDocument()
  })
})
