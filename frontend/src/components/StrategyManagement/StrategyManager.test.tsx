import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import tradingReducer from '../../store/slices/tradingSlice';
import { StrategyManager } from './StrategyManager';

const createTestStore = () => configureStore({
  reducer: {
    trading: tradingReducer,
  },
});

describe('StrategyManager', () => {
  let queryClient: QueryClient;
  let store: ReturnType<typeof createTestStore>;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
        },
      },
    });
    store = createTestStore();
  });

  it('shows loading state initially', () => {
    render(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <StrategyManager />
        </QueryClientProvider>
      </Provider>
    );

    // Verify loading states are shown initially
    expect(screen.getByTestId('strategy-list-loading')).toBeInTheDocument();
    expect(screen.getByTestId('performance-metrics-loading')).toBeInTheDocument();
  });

  it('renders strategy editor', () => {
    render(
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <StrategyManager />
        </QueryClientProvider>
      </Provider>
    );

    // Verify editor is rendered with its form elements
    expect(screen.getByTestId('strategy-editor')).toBeInTheDocument();
    expect(screen.getByTestId('max-trades-input')).toBeInTheDocument();
    expect(screen.getByTestId('stake-input')).toBeInTheDocument();
    expect(screen.getByTestId('stoploss-input')).toBeInTheDocument();
    expect(screen.getByTestId('trailing-stop-checkbox')).toBeInTheDocument();
    expect(screen.getByTestId('save-button')).toBeInTheDocument();
  });
});
