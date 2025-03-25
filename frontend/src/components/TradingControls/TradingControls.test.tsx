import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import TradingControls from './index';
import { createMockStore } from '@/tests/store';
import { startTrading, stopTrading, emergencyStop } from '@/store/slices/tradingSlice';

describe('TradingControls', () => {
  let store: any;

  beforeEach(() => {
    store = createMockStore({
      trading: {
        balance: {
          total: 100,
          free: 90,
          used: 10
        },
        totalProfit: 50,
        winRate: 0.75,
        activeTrades: 2,
        tradingEnabled: false,
        systemStatus: {
          freqtrade: true,
          database: true,
          models: true,
          quantum: false
        },
        error: null
      }
    });
  });

  it('renders trading controls in initial state', () => {
    render(
      <Provider store={store}>
        <TradingControls />
      </Provider>
    );

    expect(screen.getByText(/Trading Controls/i)).toBeInTheDocument();
    expect(screen.getByText(/Balance: £100.00/i)).toBeInTheDocument();
    expect(screen.getByText(/Win Rate: 75.00%/i)).toBeInTheDocument();
  });

  it('handles start/stop trading', () => {
    render(
      <Provider store={store}>
        <TradingControls />
      </Provider>
    );

    fireEvent.click(screen.getByText('Start Trading'));
    const actions = store.getActions();
    expect(actions[0].type).toBe('trading/startTrading/pending');

    // Update store to simulate trading enabled
    store = createMockStore({
      trading: {
        ...store.getState().trading,
        tradingEnabled: true
      }
    });

    render(
      <Provider store={store}>
        <TradingControls />
      </Provider>
    );

    fireEvent.click(screen.getByText('Stop Trading'));
    expect(store.getActions()[0].type).toBe('trading/stopTrading/pending');
  });

  it('displays error state when error occurs', () => {
    store = createMockStore({
      trading: {
        ...store.getState().trading,
        error: 'Connection failed'
      }
    });

    render(
      <Provider store={store}>
        <TradingControls />
      </Provider>
    );

    expect(screen.getByText('Connection failed')).toBeInTheDocument();
  });

  it('handles emergency stop', () => {
    render(
      <Provider store={store}>
        <TradingControls />
      </Provider>
    );

    fireEvent.click(screen.getByText('Emergency Stop'));
    const actions = store.getActions();
    expect(actions[0]).toEqual(emergencyStop());
  });
});
