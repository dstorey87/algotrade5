import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import TradingControls from './index';
import tradingReducer from '../../store/slices/tradingSlice';

const createTestStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      trading: tradingReducer
    },
    preloadedState: {
      trading: {
        balance: 10.0,
        activeStrategy: null,
        winRate: 0,
        drawdown: 0,
        trades: [],
        isTrading: false,
        lastError: null,
        ...initialState
      }
    }
  });
};

describe('TradingControls', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
  });

  it('renders trading controls in initial state', () => {
    const store = createTestStore();
    
    render(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <TradingControls />
        </QueryClientProvider>
      </Provider>
    );

    expect(screen.getByTestId('start-button')).toBeInTheDocument();
    expect(screen.getByTestId('balance-display')).toHaveTextContent('£10.00');
  });

  it('handles start/stop trading', () => {
    const store = createTestStore();
    
    render(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <TradingControls />
        </QueryClientProvider>
      </Provider>
    );

    const startButton = screen.getByTestId('start-button');
    fireEvent.click(startButton);
    
    expect(store.getState().trading.isTrading).toBe(true);
    expect(screen.getByTestId('stop-button')).toBeInTheDocument();
  });

  it('displays error state when error occurs', () => {
    const store = createTestStore({ lastError: 'API connection failed' });
    
    render(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <TradingControls />
        </QueryClientProvider>
      </Provider>
    );

    expect(screen.getByTestId('error-message')).toHaveTextContent('API connection failed');
  });
});
