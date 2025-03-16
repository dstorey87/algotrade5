import { NextResponse } from 'next/server'

// Mock data for development - will be replaced with real FreqTrade API integration
const mockStatus = {
  tradingEnabled: false,
  systemStatus: {
    freqtrade: true,
    database: true,
    models: true,
    quantum: true,
  },
  balance: {
    total: 10.00,
    free: 10.00,
    used: 0.00,
  },
  totalProfit: 0.00,
  winRate: 0.00,
  activeTrades: 0,
  trades: [
    {
      id: '1',
      pair: 'BTC/USDT',
      type: 'buy',
      amount: 0.001,
      entryPrice: 52000,
      timestamp: new Date().toISOString(),
      strategy: 'TrendFollowingML',
      confidence: 0.87,
      patternValidated: true,
      quantumValidated: true
    }
  ],
  activeStrategy: 'TrendFollowingML',
  drawdown: 0.00,
  confidence: 0.85,
  patternValidation: true,
  quantumValidation: true,
  tradesToday: 1,
  winStreak: 0,
  modelPerformance: 0.90,
  isLoading: false,
  error: null,
}

export async function GET() {
  try {
    return NextResponse.json(mockStatus)
  } catch (error: any) {
    console.error('Error fetching trading status:', error)
    return NextResponse.json(
      { error: 'Failed to fetch trading status' },
      { status: 500 }
    )
  }
}