import tradingReducer, {
  setTradingEnabled,
  setError,
  updateBalance,
  updateSystemStatus,
  emergencyStop
} from './tradingSlice';

describe('tradingSlice', () => {
  const initialState = {
    tradingEnabled: false,
    currentStrategy: null,
    balance: {
      total: 0,
      free: 0,
      used: 0
    },
    performanceStats: null,
    error: null,
    systemStatus: {
      freqtrade: false,
      database: false,
      models: false,
      quantum: false
    },
    isLoading: false,
    realTimeEnabled: false,
    isConnected: false,
    currentTrade: null,
    trades: [],
    openPositions: [],
    tradeHistory: [],
    aiMetrics: {
      accuracy: 0,
      precision: 0,
      recall: 0,
      f1Score: 0,
      latency: 0,
      ensembleAccuracy: 0,
      activeModels: 0,
      trainingInProgress: false
    }
  };

  it('should handle initial state', () => {
    expect(tradingReducer(undefined, { type: 'unknown' })).toEqual(initialState);
  });

  it('should handle setTradingEnabled', () => {
    const actual = tradingReducer(initialState, setTradingEnabled(true));
    expect(actual.tradingEnabled).toEqual(true);
  });

  it('should handle setError', () => {
    const actual = tradingReducer(initialState, setError('Test error'));
    expect(actual.error).toEqual('Test error');
  });

  it('should handle updateBalance', () => {
    const newBalance = {
      total: 100,
      free: 80,
      used: 20
    };
    const actual = tradingReducer(initialState, updateBalance(newBalance));
    expect(actual.balance).toEqual(newBalance);
  });

  it('should handle updateSystemStatus', () => {
    const newStatus = {
      freqtrade: true,
      database: true,
      models: true,
      quantum: false
    };
    const actual = tradingReducer(initialState, updateSystemStatus(newStatus));
    expect(actual.systemStatus).toEqual(newStatus);
  });

  it('should handle emergencyStop', () => {
    const state = {
      ...initialState,
      tradingEnabled: true,
      trades: [
        { id: 1, status: 'open' },
        { id: 2, status: 'closed' }
      ]
    };
    const actual = tradingReducer(state, emergencyStop());
    expect(actual.tradingEnabled).toBe(false);
    expect(actual.trades[0].status).toBe('cancelled');
    expect(actual.trades[1].status).toBe('closed');
    expect(actual.error).toBe('Emergency stop initiated - all trades cancelled');
  });
});
