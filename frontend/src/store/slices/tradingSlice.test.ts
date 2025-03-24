import tradingReducer, {
  updateBalance,
  setActiveStrategy,
  updateMetrics,
  addTrade,
  setTrading,
  setError,
  TradingState
} from './tradingSlice'

describe('tradingSlice', () => {
  const initialState: TradingState = {
    balance: 10.0,
    activeStrategy: null,
    winRate: 0,
    drawdown: 0,
    trades: [],
    isTrading: false,
    lastError: null
  }

  it('should handle initial state', () => {
    expect(tradingReducer(undefined, { type: 'unknown' })).toEqual(initialState)
  })

  it('should handle updateBalance', () => {
    const actual = tradingReducer(initialState, updateBalance(15.5))
    expect(actual.balance).toEqual(15.5)
  })

  it('should handle setActiveStrategy', () => {
    const strategy = {
      id: '1',
      name: 'Test Strategy',
      winRate: 85,
      profitFactor: 2.5,
      sharpeRatio: 1.8,
      maxDrawdown: 15,
    }
    const actual = tradingReducer(initialState, setActiveStrategy(strategy))
    expect(actual.activeStrategy).toEqual(strategy)
  })

  it('should handle updateMetrics', () => {
    const metrics = { winRate: 0.85, drawdown: 0.05 }
    const actual = tradingReducer(initialState, updateMetrics(metrics))
    expect(actual.winRate).toEqual(0.85)
    expect(actual.drawdown).toEqual(0.05)
  })

  it('should handle addTrade', () => {
    const trade = {
      id: '1',
      pair: 'BTC/USDT',
      type: 'buy',
      amount: 0.001,
      price: 50000
    }
    const actual = tradingReducer(initialState, addTrade(trade))
    expect(actual.trades).toHaveLength(1)
    expect(actual.trades[0]).toEqual(trade)
  })

  it('should handle setTrading', () => {
    const actual = tradingReducer(initialState, setTrading(true))
    expect(actual.isTrading).toBe(true)
  })

  it('should handle setError', () => {
    const errorMessage = 'API connection failed'
    const actual = tradingReducer(initialState, setError(errorMessage))
    expect(actual.lastError).toEqual(errorMessage)
  })
});
